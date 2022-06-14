import argparse
import itertools
import logging
from multiprocessing.pool import ThreadPool
from urllib.parse import quote_plus

import requests
from retry import retry
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--api-key",
        help="Scraping Fish API key",
        required=True,
        type=str,
    )
    parser.add_argument(
        "--urls",
        help="Path to a file with the list of urls to scrape",
        required=True,
        type=str,
    )
    parser.add_argument(
        "--api",
        help="Scraping Fish API url",
        required=False,
        type=str,
        default="https://scraping.narf.ai/api/v1/?",
    )
    parser.add_argument(
        "--concurrency",
        help="Number of concurrent connections",
        required=False,
        type=int,
        default=1,
    )
    parser.add_argument(
        "--retries",
        help="Number of retries in case of unsuccessful response",
        required=False,
        type=int,
        default=2,
    )
    parser.add_argument(
        "--timeout",
        help="How many seconds to wait for the server to respond before giving up",
        required=False,
        type=float,
        default=30.0,
    )
    parser.add_argument(
        "--limit",
        help="Limit the number of URLs to scrape (set to 0 to disable)",
        required=False,
        type=int,
        default=0,
    )
    parser.add_argument(
        "--render-js",
        help="Enable JS rendering",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--verbose",
        help="Verbose mode",
        action="store_true",
        default=False,
    )
    return parser.parse_args()


class ScrapingErrorException(Exception):
    pass


class ScrapingBlockedException(Exception):
    pass


def got_blocked(status_code, resolved_url, body):
    # Implement custom logic to detect blocked request in this function
    if status_code == 429:
        return True
    blocked_messages = [
        "Server responded with 429",
        "automated queries",
        "Amazon CAPTCHA",
    ]
    if any([m in body for m in blocked_messages]):
        return True
    if "/accounts/login/" in resolved_url:
        return True
    return False


def process_results(results):
    # Your result processing logic goes here
    pass


def main(args):
    logging.basicConfig(level=logging.WARNING if args.verbose else logging.ERROR)
    logger = logging.getLogger()

    with open(args.urls, "r") as file:
        urls = file.read().splitlines()

    url_prefix = f"{args.api}api_key={args.api_key}&render_js={str(args.render_js).lower()}&url="

    error = 0
    blocked = 0
    success = 0

    stop = len(urls) if args.limit == 0 else args.limit
    url_loader = itertools.islice(itertools.cycle(urls), stop)

    with tqdm(url_loader, unit="url", total=stop) as progress:
        progress.set_description(f"Concurrency={args.concurrency}")

        @retry(Exception, tries=args.retries, logger=logger)
        def scrape(url):
            encoded_url = quote_plus(url)
            response = requests.get(f"{url_prefix}{encoded_url}", timeout=args.timeout)
            status_code = response.status_code
            resolved_url = response.url
            body = response.text
            if got_blocked(status_code, resolved_url, body):
                raise ScrapingBlockedException((url, status_code))
            if status_code == 404:
                logger.warning((url, status_code))
                return body
            if not (200 <= status_code <= 299):
                raise ScrapingErrorException((url, status_code))
            return body

        def monitor_scrape(url):
            nonlocal error, blocked, success
            response_body = ""
            try:
                response_body = scrape(url)
                success += 1
            except ScrapingBlockedException as e:
                logger.warning(repr(e))
                blocked += 1
            except (ScrapingErrorException, Exception) as e:
                logger.warning(url)
                logger.warning(repr(e))
                error += 1
            finally:
                progress.update()
                progress.set_postfix_str(
                    f"Success={success}, Error={error}, Blocked={blocked}"
                )
            return response_body

        with ThreadPool(args.concurrency) as pool:
            results = pool.map(monitor_scrape, url_loader)
        
        process_results(results)


if __name__ == "__main__":
    main(parse_args())
