#!/usr/bin/env python3

import ast
from abc import ABC, abstractmethod

class Scraper(ABC):
    """Abstract class for all scrapers.

    This class should be inherited and overridden with customer specific scraping code.
    """
    def __init__(self, raw_data):
        # Initialize data dict
        self._scraped_data = {
            "usage": None,
            "bill": None,
            "service_start": None,
            "service_end": None,
            "due_date": None
        }

        # Perform actual extraction
        self._scrape_all(raw_data)

    #-------------------------------------- Public ------------------------------------------------

    def get_usage(self):
        """Return extracted usage (kWh) for the current bill.
        """
        return self._scraped_data["usage"]

    def get_bill(self):
        """Return extracted amount ($) for the current bill.
        """
        return self._scraped_data["bill"]

    def get_service_start(self):
        """Return extracted service start date of the current bill.
        """
        return self._scraped_data["service_start"]

    def get_service_end(self):
        """Return extracted service end date of the current bill.
        """
        return self._scraped_data["service_end"]

    def get_due_date(self):
        """Return extracted due date of the current bill.
        """
        return self._scraped_data["due_date"]

    #------------------------------------- Private ------------------------------------------------

    @abstractmethod
    def _scrape_all(self, raw_data):
        """Private abstract method to perform all scraping.
        """
        pass

class DominionScraper(Scraper):
    """Dominion Energy specific scraper.
    """
    def __init__(self, raw_data):
        super().__init__(raw_data)

    def _scrape_all(self, raw_data):
        """Private method to perform all scraping.

        This is the workhorse of this class; it's customized for dominion energy specifically.
        This class should do everything necessary to populate the self._scraped_data class.

        Args:
            raw_data:   A BeautifulSoup formatted HTML object extracted from Dominion Energy.

        """
        # get home page content (where all the data we care about is located)
        homepageContent = raw_data.find_all("div", {"id": "homepageContent"})[0]

        # brute force: step through the home page and extract all bill information
        bill_due_flag = False
        for element in homepageContent:
            # skip all unnamed elements
            if element.name is None:
                continue

            # Check if flags are true; that means there's data in this element!
            if bill_due_flag:
                # extract bill and due date data:

                spans = element.find_all(class_="bodyTextGreen")
                self._scraped_data["due_date"] = spans[0].contents[0]
                self._scraped_data["bill"] = spans[1].contents[0]

                # we're done; break out of the loop
                break

            # Check if any flags should be activated
            if ["Total Amount Due By"] in [e.contents for e in element.find_all("h5")]:
                # next element contains the bill and due date
                bill_due_flag = True
                
        # extract meter read data and usage from given chart
        graph_data = homepageContent.find("input", {"id": "UsageDataArrHdn"})
        graph_dates = homepageContent.find("input", {"id": "UsageDateArrHdn"})

        # safely convert to list
        graph_data = ast.literal_eval(graph_data.get("value"))
        graph_dates = graph_dates.get("value").split(",")

        # populate data
        self._scraped_data["usage"] = graph_data[0][1]
        self._scraped_data["service_end"] = graph_dates[0]
        self._scraped_data["service_start"] = graph_dates[1]
