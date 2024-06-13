import requests
import pandas as pd
import time
import os

# Constantly sends data to kafka stream
def read_csv_and_send_data(file_path, api_url):
    df = pd.read_csv(file_path)

    for _, row in df.iterrows():
        transaction = row.to_dict()
        response = requests.post(api_url, json=transaction)
        if response.status_code == 200:
            print(f"Sent: {transaction}")
        else:
            print(f"Failed to send: {transaction}")
        time.sleep(1)

if __name__ == "__main__":
    data_path = './data/creditcard.csv'
    api_url = os.getenv('API_GATEWAY_URL', 'http://localhost:8000/transactions/')
    read_csv_and_send_data(data_path, api_url)