#!/usr/bin/env python3

import copy
from bs4 import BeautifulSoup
import requests

class DominionCrawler:
    """Class designed to extract HTML data from the given webpage.
    """

    def __init__(self):
        # helpful class variables
        self._default_timeout = 10

        # this dict contains most of the data required to login
        self._login_url = "https://mydom.dominionenergy.com/siteminderagent/forms/login.fcc"
        self._login_payload = {
            "PASSWORD": None,
            "USER": None,
            "postpreservationdata": None,
            "smauthreason": "0",
            "SMLOCALE": "US-EN",
            "smusrmsg": None,
            "target": "https://mydom.dominionenergy.com/",
            "smagentname": None
        }

        # Start a persistent session
        self._session = requests.session()
    
    def login(self, username, password):
        """Login to the given URL.

        Args:
            username:   The username to login with.
            password:   The password to login with.
        """
        # Attempt to login
        try:
            payload = copy.deepcopy(self._login_payload)
            payload["USER"] = username
            payload["PASSWORD"] = password

            page_response = self._session.post(self._login_url, 
                                               data=payload, 
                                               headers=dict(referer=self._login_url), 
                                               timeout=self._default_timeout)
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Connection failed; are you connected to the internet?")
        except requests.exceptions.ReadTimeout:
            raise RuntimeError("Request failed to load withing %s seconds." % str(self._default_timeout))

        # parse request into usable format
        page_content = BeautifulSoup(page_response.content, "html.parser")

        return page_content
