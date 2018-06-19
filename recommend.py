# -*- coding: utf-8 -*-

import pandas as pd
from slack import Slack


def check_exists_similarity(data: pd.DataFrame) -> bool:
    if data.columns.isin(['similarity']).any():
        return True
    else:
        return False


def extract_most_similar_paper(data: pd.DataFrame) -> pd.DataFrame:
    if not check_exists_similarity(data):
        raise ValueError('data must contain "similarity" in its column.')
    similarity = data.similarity
    is_most_similar = similarity == similarity.max()
    return data.loc[is_most_similar, :].copy()


def extract_most_dissimilar_paper(data: pd.DataFrame) -> pd.DataFrame:
    if not check_exists_similarity(data):
        raise ValueError('data must contain "similarity" in its column.')
    data_exclude_zero = data.loc[data.similarity > 0, :]
    similarity = data_exclude_zero.similarity
    is_most_dissimilar = similarity == similarity.min()
    return data_exclude_zero.loc[is_most_dissimilar, :].copy()


# TODO: implement displaying the authors
MESSAGE = """*Today's most {recommend_type} paper of your interest*
Title: {title}
URL: {link}
Descriptions:
>>> {description}
"""


def generate_recommend_message(data: pd.DataFrame, recommend_type: str) -> str:
    return MESSAGE.format(recommend_type=recommend_type,
                          title=data.title.values[0],
                          link=data.link.values[0],
                          description=data.description.values[0])


def recommend(data: pd.DataFrame) -> object:
    slack = Slack()

    most_similar = extract_most_similar_paper(data)
    most_similar_message = generate_recommend_message(
        data=most_similar,
        recommend_type='similar'
    )
    slack.post_message(most_similar_message)

    most_dissimilar = extract_most_dissimilar_paper(data)
    most_dissimilar_message = generate_recommend_message(
        data=most_dissimilar,
        recommend_type='dissimilar'
    )
    slack.post_message(most_dissimilar_message)

