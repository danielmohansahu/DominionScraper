#!/usr/bin/env python3

import code
from getpass import getpass

from dominion_scraper.crawler import DominionCrawler
from dominion_scraper.scraper import DominionScraper

if __name__ == "__main__":
    # Instantiate crawler
    crawler = DominionCrawler()

    # login and extract raw data:
    # @todo force user input
    data = crawler.login(
        getpass("Username: "),
        getpass("Password: ")
    )

    # perform data extraction
    scraper = DominionScraper(data)

    # print outputs:
    output_str = "\nBill information:" \
        + "\n\tBill ($):\t{}".format(scraper.get_bill()) \
        + "\n\tUsage (kWh):\t{}".format(scraper.get_usage()) \
        + "\n\tStart:\t\t{}".format(scraper.get_service_start()) \
        + "\n\tEnd:\t\t{}".format(scraper.get_service_end()) \
        + "\n\tDue:\t\t{}\n".format(scraper.get_due_date())
    print(output_str)

    code.interact(local=locals())

