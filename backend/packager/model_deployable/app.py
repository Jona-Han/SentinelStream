from flask import Flask
import time

app = Flask(__name__)

@app.route("/predict")
def predict():
    time.sleep(0.25)
    return {
        "value": "PredictionClass" 
    }