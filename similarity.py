# -*- coding: utf-8 -*-

import json
import nltk


with open('test.json', 'r', encoding='utf-8') as f:
    line = f.readline()
    data = json.loads(line)

description = data['description']
