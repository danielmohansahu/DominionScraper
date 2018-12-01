# Dominion Scraper

This package contains a web scraper / crawler pair for extracting billing information from a Dominion Energy user account. Usage requires credentials to a valid Dominion Energy customer account.

### Prerequisites

This code runs on python3. The only non-standard library is BeautifulSoup (bs4).

```bash
pip3 install bs4
```

## Example Usage

Assuming the package is on your path:

```python
from dominion_scraper.crawler import DominionCrawler
from dominion_scraper.scraper import DominionScraper

# Instantiate crawler
crawler = DominionCrawler()

# login and extract raw data:
data = crawler.login(
    "MY-USERNAME",
    "MY-PASSWORD"
)

# perform data extraction
scraper = DominionScraper(data)

# access data:
scraper.get_usage()     # returns usage (kWh) for the current billing cycle
scraper.get_bill()      # returns bill ($)
...
```

See `example.py` for more usage information.
