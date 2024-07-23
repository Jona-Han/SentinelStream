import os
from dotenv import load_dotenv
from message_handler import MessageHandler
import six
import sys
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves


def main():
    KAFKA_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
    conn_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }

    # Check for missing environment variables
    if missingEnvVariables(KAFKA_SERVERS, KAFKA_TOPIC, conn_params):
        print("MISSING VARIABLES")
        return
    
    try:
        messageProxy = MessageHandler(KAFKA_TOPIC, KAFKA_SERVERS, conn_params)
        messageProxy.start_listening()
    except Exception as e:
        print(f'Error occurred: {e}')
        return
    print('Training service complete.')

def missingEnvVariables(KAFKA_SERVERS, KAFKA_TOPIC, conn_params):
    if not KAFKA_SERVERS:
        print('KAFKA_BOOTSTRAP_SERVERS environment variable is missing.')
        return True
    if not KAFKA_TOPIC:
        print('KAFKA_TOPIC environment variable is missing.')
        return True
    for key, value in conn_params.items():
        if not value:
            print(f'{key} environment variable is missing.')
            return True
    return False

if __name__ == "__main__":
    try:
        load_dotenv()
        main()
    except:
        print("ERROR: problem running dot_env or main")
