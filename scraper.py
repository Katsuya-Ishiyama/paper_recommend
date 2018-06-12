# -*- coding: utf-8 -*-

import logging

import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://arxiv.org/rss/{category}'
CATEGORIES = ['cs']

logger = logging.getLogger('scraper')


class Scraper(object):

    def __init__(self):
        self.base_url = 'http://arxiv.org/rss/{field}'
        self.field = None
        self.response = None
        self.parsed_html = None

    @property
    def url(self):
        """
        getter of url

        Returns
        -------
        url of arXiv's rss
        """
        return self.base_url.format(field=self.field)

    def fetch_rss(self, field: str):
        """ fetch rss from arXiv

        Arguments
        ---------
        field : str
            field of your expertise. (eg. stat, cs)

        Returns
        -------
        html parsed by BeautifulSoup
        """
        self.field = field
        _url = self.url
        _response = requests.get(_url)
        _status_code = _response.status_code
        if _status_code != 200:
            logging.warning('{} status code: {}'.format(_url, _status_code))
            raise requests.HTTPError(_status_code)
        else:
            self.response = _response
        self.parsed_html = BeautifulSoup(self.response.text, 'lxml')

    def extract_item(self):
        self.parsed_html.select('#collapsible6')
        return self.parsed_html.find_all('item')

    def extract_authors(self):
        return self.parsed_html.find_all('creator')

    def extract_title(self):
        return self.parsed_html.find_all('title')

    def extract_description(self):
        return self.parsed_html.find_all('description')


if __name__ == '__main__':
    scraper = Scraper()
    scraper.fetch_rss(field='stat')
    authors = scraper.extract_authors()
    titles = scraper.extract_title()
    descriptions = scraper.extract_description()
    for a, t, d in zip(authors, titles, descriptions):
        print(a, t, d)
        print()
