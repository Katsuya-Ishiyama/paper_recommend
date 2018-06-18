# -*- coding: utf-8 -*-

import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_paper_summaries_from_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        paper_summaries = [json.loads(line) for line in f]
    return paper_summaries


test_query = 'I want to predict mascots\' popularity from its photo using machine learning methodologies.'

descriptions = [test_query]
paper_summaries = load_paper_summaries_from_json('.\\test\\test.json')
for summary in paper_summaries:
    descriptions.append(summary['description'])
