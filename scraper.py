# -*- coding: utf-8 -*-

import logging
import re
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag


logger = logging.getLogger('RSSScraper')


class RSSScraper(object):

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
        self._metadata_src = self.parsed_html.findAll('channel')[0]
        self._abstract_src = self.parsed_html.find_all('item')

    def _extract_metadata_internal(self, category: str) -> str:
        """
        Extract metadata from fetched html.

        Arguments
        ---------
        category: str
            category of metadata. eg: date, publisher etc.

        Returns
        -------
        extracted metadata. all data types are str.
        """
        target_tag = '<dc:{category}>'.format(category=category)
        _meta = None
        for content in self._metadata_src.contents:
            if target_tag in str(content):
                _meta = content.text
                break
        return _meta

    def extract_metadata(self):
        """ extract metadata from fetched html. """
        _meta = {
            'date': self._extract_metadata_internal('date'),
            'lang': self._extract_metadata_internal('language'),
            'publisher': self._extract_metadata_internal('publisher'),
            'subject': self._extract_metadata_internal('subject')
        }
        return _meta

    def extract_paper_abstract(self):
        _metadata = self.extract_metadata()
        for tag in self._abstract_src:
            abstract = {
                'title': self._extract_title(tag),
                'description': self._extract_description(tag),
                'link': self._extract_link(tag),
                'authors': self._extract_authors(tag)
            }
            abstract.update(_metadata)
            yield abstract

    def _extract_title(self, tag: Tag) -> str:
        return tag.title.text

    def _extract_description(self, tag: Tag) -> str:
        desc = tag.description.text
        soup = BeautifulSoup(desc.replace('\n', ' '), 'xml')
        normalised = soup.text
        return normalised

    def _extract_link(self, tag: Tag) -> str:
        link = re.findall(r'<link/>(.*)\n', str(tag))[0]
        return link

    def _extract_authors(self, tag: Tag) -> str:
        creators = re.findall(r'<dc:creator>(.*)</dc:creator>', str(tag))[0]
        creators_xml = creators.replace('&lt;', '<')
        creators_xml = creators_xml.replace('&gt;', '>')
        soup = BeautifulSoup(creators_xml, 'lxml')
        tags = soup.findAll('a')
        authors = [{'name': t.text, 'link': t.get('href')} for t in tags]
        return authors
