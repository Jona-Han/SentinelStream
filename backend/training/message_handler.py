import json

from kafka import KafkaConsumer

from database_handler import DatabaseHandler
from model_trainer import ModelTrainer

class MessageHandler:
    def __init__(self, topic, servers, db_params):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=servers,
            max_poll_records = 100,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        self.db_handler = DatabaseHandler(db_params)

    def start_listening(self):
        while True:
            for message in self.consumer:
                print(message.value)
                trainer = ModelTrainer(message.input_dataset_uuid, message.training_params_uuid, self.db_handler)
                trainer.process()
                print("complete")