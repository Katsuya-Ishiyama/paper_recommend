# -*- coding: utf-8 -*-

import pandas as pd

def recommend(data: pd.DataFrame):
	similarity = data.similarity
	is_most_similar = similarity == similarity.max()
	return data.loc[is_most_similar, :].copy()
