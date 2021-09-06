import logging
import json
import psycopg2

from psycopg2.extras import DictCursor
from queries import get_entity_ids, get_related_filmwork_ids, get_data_for_load
from utils import backoff


class Reader:
    def __init__(self, receiver, dsl_path, start_date, entity):
        self.logger = logging.getLogger("log")
        self.start_date = start_date
        self.end_date = self.start_date
        self.receiver = receiver
        self.dsl_path = dsl_path
        self.entity = entity

    @backoff(exception=psycopg2.OperationalError, border_sleep_time=100)
    def establish_connection(self):
        logging.info("establishing connection to postgres")
        self.conn = psycopg2.connect(**self.dsl(), cursor_factory=DictCursor)
        logging.info("connection established")

    def dsl(self):
        with open(self.dsl_path, 'r') as f:
            j = json.load(f)
        return j

    def send_data(self, data):
        """
        Формирует из данных бд батчи,
        содержащие данные об одном конкретном film_work,
        отправляет батчи следующему компоненту системы.
        """
        batch = []
        batch_id = data[0]['fw_id']
        for rec in data:
            if rec['fw_id'] != batch_id:
                self.receiver.send(batch)
                batch_id = rec['fw_id']
                batch = []
            batch.append(rec)

    def run(self):
        """
        Получает из бд данные о необновлённых entity,
        получает данные о связанных film_work,
        отправляет следующему компоненту системы
        """
        with self.conn.cursor() as cur:
            cur.execute(get_entity_ids.format(start_date=self.start_date,
                                              entity=self.entity))
            entity_data = cur.fetchall()

            entity_ids = tuple(rec['id'] for rec in entity_data)
            self.end_date = entity_data[-1]['modified']

            if self.entity in ('genre', 'person'):
                cur.execute(get_related_filmwork_ids.format(entity_ids=entity_ids,
                                                            entity=self.entity))
                filmwork_ids = tuple(rec['id'] for rec in cur.fetchall())
            elif self.entity == 'film_work':
                filmwork_ids = entity_ids

            cur.execute(get_data_for_load.format(filmwork_ids))
            data = cur.fetchall()
            if data:
                self.send_data(data)
