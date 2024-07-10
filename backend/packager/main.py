import os
from dotenv import load_dotenv
from message_handler import MessageHandler
import six
import sys
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

def main():
    print('Containerization service starting.')
    KAFKA_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
    conn_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }

    if not KAFKA_SERVERS or not KAFKA_TOPIC or not conn_params:
        print('Environment variables missing.')
        return
    
    messageProxy = MessageHandler(KAFKA_TOPIC, KAFKA_SERVERS, conn_params)
    messageProxy.start_listening()
    print('Containerization service complete.')

if __name__ == '__main__':
    load_dotenv()
    main()