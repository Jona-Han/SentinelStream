import os

from message_handler import MessageHandler

def main():
    KAFKA_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')

    if not KAFKA_SERVERS or not KAFKA_TOPIC:
        print('Environment variables missing.')
        return
    
    messageProxy = MessageHandler(KAFKA_TOPIC, KAFKA_SERVERS)
    messageProxy.start_listening()

    print('Containerization service complete.')

if __name__ == '__main__':
    main()