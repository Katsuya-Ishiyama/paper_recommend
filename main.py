# -*- coding: utf-8 -*-

import argparse
import pandas as pd
from recommend import recommend
from scraper import RSSScraper
from similarity import calculate_similarity_of_interest


def get_commandline_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fields',
                        type=str,
                        required=True,
                        nargs='+',
                        help='Your interested fields.')
    return parser.parse_args()


def main():
    # TODO: revise to receive interest from a foreign source.
    interest = ['I want to predict mascots\' popularity from its photo using machine learning methodologies.']

    args = get_commandline_args()
    scraper = RSSScraper()
    _papers = []
    descriptions = []
    for field in args.fields:
        scraper.fetch_rss(field=field)
        for _abs in scraper.extract_paper_abstract():
            _papers.append(_abs)
            descriptions.append(_abs['description'])

    papers = pd.DataFrame(data=_papers)
    similarity = pd.Series(
        data=calculate_similarity_of_interest(
            interest=interest,
            descriptions=descriptions
        )
    )
    papers.loc[:, 'similarity'] = similarity

    recommend(papers, interest)


if __name__ == '__main__':
    main()
