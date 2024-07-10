import json

from kafka import KafkaConsumer

from backend.training.model_trainer import ModelTrainer

class MessageHandler:
    def __init__(self, topic, servers, model_params, db_params):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=servers,
            max_poll_records = 100,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        self.model_params = model_params
        self.db_params = db_params

    def start_listening(self):
        for message in self.consumer:
            print(json.loads(message.value))
            trainer = ModelTrainer(self.model_params, self.db_params)
            trainer.process()