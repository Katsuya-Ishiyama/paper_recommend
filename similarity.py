# -*- coding: utf-8 -*-

import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_paper_summaries_from_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        paper_summaries = [json.loads(line) for line in f]
    return paper_summaries


interest = ['I want to predict mascots\' popularity from its photo using machine learning methodologies.']

paper_summaries = load_paper_summaries_from_json('.\\test\\test.json')
descriptions = [summary['description'] for summary in paper_summaries]
corpus = interest + descriptions

vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words='english')
tfidf_matrix = vectorizer.fit_transform(corpus).toarray()
interest_tfidf_matrix = tfidf_matrix[0, :]
descriptions_tfidf_matrix = tfidf_matrix[1:, :]
similarity = cosine_similarity(interest_tfidf_matrix, descriptions_tfidf_matrix)[0].tolist()

#for i, summary in enumerate(paper_summaries):
#    summary.update({'similarity': similarity[i]})

paper_summaries_table = pd.DataFrame(data=paper_summaries)
paper_summaries_table.loc[:, 'similarity'] = pd.Series(similarity)
is_max = paper_summaries_table.similarity == paper_summaries_table.similarity.max()
paper_summaries_table.loc[is_max, :]
