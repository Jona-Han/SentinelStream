import json

from kafka import KafkaConsumer

from packager import Packager
from database_handler import DatabaseHandler

class MessageHandler:
    def __init__(self, topic, servers, db_params):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=servers,
            max_poll_records = 100,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        self.db_handler = DatabaseHandler(db_params)

    def start_listening(self):
        for message in self.consumer:
            print(message.value)
            packager = Packager(message.model_uuid, self.db_handler)
            packager.process()