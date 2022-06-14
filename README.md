# Web scraping API benchmark by Scraping Fish 🐟

This repository contains python code used to benchmark web scraping APIs.

The results are presented at https://scrapingfish.com/webscraping-benchmark.

You can also use the script from this repository to run a scraping job with Scraping Fish API by providing an input file with a list of URLs to scrape.
Possible configuration options are documented in the Usage section below.

## Prerequisites

To run the code, you need to install dependencies:

```
pip install -r requirements.txt
```

## Input

For input, you have to prepare a text file with a list of URLs separated by new line character.

Example input files with URLs provided in the `urls` folder used for the benchmark:
- `alexa.txt`: URLs from the top 1,000 Alexa rank
- `amazon.txt`: Amazon product URLs
- `google.txt`: Google search queries
- `instagram.txt`: the top 10 Instagram profiles (as of 2022)
- `similarweb.txt`: websites from the similarweb ranking (excluding adult and russian websites)

## Usage

Run `main.py` script with `--help` argument to show usage options.

```
$ python main.py --help
usage: main.py [-h] --api-key API_KEY --urls URLS [--api API] [--concurrency CONCURRENCY] 
               [--retries RETRIES] [--timeout TIMEOUT] [--limit LIMIT] [--render-js] [--verbose]

optional arguments:
  -h, --help                 show this help message and exit
  --api-key API_KEY          Scraping Fish API key
  --urls URLS                Path to a file with the list of urls to scrape
  --api API                  Scraping Fish API url
  --concurrency CONCURRENCY  Number of concurrent connections
  --retries RETRIES          Number of retries in case of unsuccessful response
  --timeout TIMEOUT          How many seconds to wait for the server to respond before giving up
  --limit LIMIT              Limit the number of URLs to scrape (set to 0 to disable)
  --render-js                Enable JS rendering
  --verbose                  Verbose mode
```

## Example

To run a job for scraping Amazon product URLs
- using 5 concurrent connections,
- with 2 retries after the request fails or times out,
- interrupting unfinished request after 60 seconds.

```
python main.py --api-key <YOUR_SCRAPING_FISH_API_KEY> --urls ./urls/amazon.txt \
               --concurrency 5 --retries 2 --timeout 60
```

## Benchmark methodology

We run scraping jobs for the 5 example input files in the `urls` folder by making 1,000 requests for each of them.
Concurrency and response timeout parameters were set to achieve optimal processing time and keep the error rate low.

> 📝 If you want to use this script for your web scraping job, you might need to adjust these parameters to the websites you want to scrape.

For the benchmark, we executed the following commands.

### Alexa

```
python main.py --api-key API_KEY --urls ./urls/alexa.txt \
               --concurrency 5 --timeout 60.0  --limit 1000
```

### Amazon

```
python main.py --api-key API_KEY --urls ./urls/amazon.txt \
               --concurrency 5 --timeout 15.0  --limit 1000
```

### Google

```
python main.py --api-key API_KEY --urls ./urls/google.txt \
               --concurrency 5 --timeout 15.0  --limit 1000
```

### Instagram

```
python main.py --api-key API_KEY --urls ./urls/instagram.txt \
               --concurrency 2 --timeout 60.0  --limit 1000
```

### Similarweb

```
python main.py --api-key API_KEY --urls ./urls/similarweb.txt \
               --concurrency 5 --timeout 15.0  --limit 1000
```

### Metrics

For each test, we recorded
- ✅ successful URLs
- ❌ failed URLs
- ⛔️ blocked URLs
- ⏱ average URL processing time (seconds/URL)
- 💰 cost of running the benchmark (1000 requests)

The results are presented in the section below.

## Results

### Scraping Fish 🐟

| Test       | ✅ Successful | ❌ Failed | ⛔️ Blocked | ⏱ Processing time |  💰 Cost |
|------------|-------------:|---------:|----------:|------------------:|--------:|
| Alexa      |        99.9% |     0.1% |        0% |              2.63 |      $2 |
| Amazon     |       100.0% |       0% |        0% |              3.37 |      $2 |
| Google     |       100.0% |       0% |        0% |              1.63 |      $2 |
| Instagram  |        97.0% |     3.0% |        0% |             23.25 |      $2 |
| Similarweb |       100.0% |       0% |        0% |              2.50 |      $2 |
| **Total**  |    **99.4%** | **0.6%** |  **0.0%** |          **6.28** | **$10** |

> 📝 $0.002 per each successfully scraped URL. The highest overall success rate and the best processing time.

### Other web scraping APIs

#### ScrapingAnt 🐜

Benchmarks run using `--api "https://api.scrapingant.com/v1/general/?proxy_type=residential&"` parameter and adjusted code to pass API key as a header instead of query parameter.

| Test       | ✅ Successful | ❌ Failed | ⛔️ Blocked | ⏱ Processing time |  💰 Cost |
|------------|-------------:|---------:|----------:|------------------:|--------:|
| Alexa      |       100.0% |       0% |        0% |              6.92 |     $19 |
| Amazon     |        98.0% |     2.0% |        0% |              9.84 |     $19 |
| Google     |        95.0% |     5.0% |        0% |             13.80 |     $19 |
| Instagram  |        99.5% |     0.5% |        0% |              6.76 |     $19 |
| Similarweb |        96.0% |     4.0% |        0% |              7.40 |     $19 |
| **Total**  |    **97.7%** | **2.3%** |  **0.0%** |          **8.94** | **$49** |

> 📝 $49 Startup subscription required to scrape 5,000 URLs in total (each consuming 50 or 250 API credits) and using 5 concurrent connections.

#### ScrapingBee 🐝

Benchmarks run using `--api "https://app.scrapingbee.com/api/v1/?premium_proxy=true&"` and `custom_google` parameter set to true for Google benchmark.

| Test       | ✅ Successful | ❌ Failed | ⛔️ Blocked | ⏱ Processing time |  💰 Cost |
|------------|-------------:|---------:|----------:|------------------:|--------:|
| Alexa      |        81.0% |    18.0% |      1.0% |              4.86 |     $99 |
| Amazon     |        99.0% |     1.0% |        0% |             11.48 |     $99 |
| Google     |       100.0% |       0% |        0% |              3.74 |     $99 |
| Instagram  |        99.0% |     1.0% |        0% |             18.52 |     $99 |
| Similarweb |        90.0% |     8.0% |      2.0% |              4.70 |     $99 |
| **Total**  |    **93.8%** | **5.6%** |  **0.6%** |          **8.66** | **$99** |

> 📝 $99 Startup subscription required to scrape 5,000 URLs in total (each consuming 10, 20, or 25 API credits) and using 5 concurrent connections.

#### ScraperAPI

Benchmarks run using `--api "http://api.scraperapi.com/?premium=true&"` parameter.

| Test                  | ✅ Successful | ❌ Failed | ⛔️ Blocked | ⏱ Processing time |  💰 Cost |
|-----------------------|-------------:|----------:|----------:|------------------:|--------:|
| Alexa                 |        95.5% |      4.5% |        0% |              7.19 |     $49 |
| Amazon                |        96.0% |      4.0% |        0% |             10.97 |     $49 |
| Google                |       100.0% |        0% |        0% |              4.50 |     $49 |
| Instagram<sup>*</sup> |         0.0% |    100.0% |        0% |                 - |       - |
| Similarweb            |        90.0% |      8.0% |      2.0% |              4.70 |     $49 |
| **Total**             |    **76.3%** | **23.3%** |  **0.4%** |          **6.84** | **$49** |

> <sup>*</sup> Scraping Instagram is not allowed and returns 403 status code.

> 📝 $49 Hobby subscription required to scrape 5,000 URLs in total (each consuming 10 or 25 API credits) and using 5 concurrent connections.

## Try it with Scraping Fish API

To run the scraping script, you need to get your Scraping Fish API key [here](https://scrapingfish.com/buy).
