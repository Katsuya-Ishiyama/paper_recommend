# -*- coding: utf-8 -*-

import logging

import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://arxiv.org/rss/{category}'
CATEGORIES = ['cs']

logger = logging.getLogger('scraper')

category = CATEGORIES[0]

url = BASE_URL.format(category=category)
response = requests.get(url)

status_code = response.status_code
if status_code != 200:
    logging.warning('{} status code: {}'.format(url, status_code))
    raise requests.HTTPError(status_code)

soup = BeautifulSoup(response.text, 'lxml')
