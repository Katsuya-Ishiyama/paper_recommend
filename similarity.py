# -*- coding: utf-8 -*-

import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity_of_interest(interest, descriptions):
    corpus = interest + descriptions
    vectorizer = TfidfVectorizer(ngram_range=(1, 3),
                                 stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus).toarray()
    interest_tfidf_matrix = tfidf_matrix[0, :]
    descriptions_tfidf_matrix = tfidf_matrix[1:, :]

    similarity = cosine_similarity(X=interest_tfidf_matrix.reshape(1, -1),
                                   Y=descriptions_tfidf_matrix)
    return similarity[0].tolist()
