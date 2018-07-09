# -*- coding: utf-8 -*-

import json
import requests
import yaml


class Slack(object):
    def __init__(self):
        self._conf = self.load_conf()

    def load_conf(self) -> dict:
        with open('paper_recommend/.slack_conf.yaml', 'r') as f:
            _conf = yaml.load(f)
        return _conf

    def post_message(self, message: str) -> object:
        url = self._conf['webhook']['url']
        requests.post(url=url, data=json.dumps({'text': message}))
