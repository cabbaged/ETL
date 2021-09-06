import argparse
import configparser
import json
import logging

from datetime import datetime
from reader import Reader
from sender import sender
from transformer import transformer
from utils import establish_logger


def get_state(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def update_state(file_path, state):
    with open(file_path, 'w') as f:
        json.dump(state, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--entity', required=True)
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)
    dsl_path = config.get('main', 'pg_dsl_path')
    state_path = config.get(args.entity, 'state_path')
    url = config.get('main', 'es_url')

    establish_logger()

    state = get_state(state_path)
    logging.info('acquired state: ' + str(state))

    s = sender(url, state)
    t = transformer
    r = Reader(receiver=t(s),
               dsl_path=dsl_path,
               start_date=datetime.fromisoformat(state['state']),
               entity=args.entity
               )
    r.establish_connection()
    r.run()

    try:
        s.send('finish')
    except StopIteration:
        logging.info('writing state: ' + str(state))
        state['state'] = r.end_date.isoformat()
        update_state(state_path, state)
