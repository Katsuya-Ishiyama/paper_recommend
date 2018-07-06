# -*- coding: utf-8 -*-

import os
import json
import requests


class Slack(object):
    def __init__(self):
        self._webhook = os.environ['SLACK_WEBHOOK']

    def post_message(self, message: str) -> object:
        requests.post(url=self._webhook, data=json.dumps({'text': message}))

