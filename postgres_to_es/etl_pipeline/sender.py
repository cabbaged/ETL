import logging
import requests
import json

from utils import coroutine, backoff


@backoff(exception=requests.exceptions.ConnectionError, border_sleep_time=100)
def send(url, data):
    headers = {'Content-Type': 'application/json'}
    logging.info("sending data to es")
    requests.post(url,
                  data=json.dumps(data, default=str),
                  headers=headers)


@coroutine
def sender(base_url, state):
    url_pattern = base_url + '/filmwork/_doc/{fw_id}?pretty'
    while data := (yield):
        if data == 'finish':
            logging.info('finishing send')
            break
        url = url_pattern.format(fw_id=data['fw_id'])
        send(url, data)
        state['state'] = data['modified']
