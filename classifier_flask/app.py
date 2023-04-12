## index.py
from flask import Flask, jsonify, request
import torch
from pred import ClassPredictor
from transformers import AutoTokenizer, XLMRobertaForSequenceClassification
import os 
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Load XLM-RoBERTa tokenizer and model
model_lax = XLMRobertaForSequenceClassification.from_pretrained("GuneetK/mh-nmh-lax",num_labels=2,from_tf=False)
model_strict = XLMRobertaForSequenceClassification.from_pretrained("GuneetK/mh-nmh-strict",num_labels=2,from_tf=False)
tokenizer = AutoTokenizer.from_pretrained("GuneetK/mh-nmh-tokenizer")

predictor_lax = ClassPredictor(model_lax,tokenizer)
predictor_strict = ClassPredictor(model_strict,tokenizer)

@app.route("/")
def index():
    return jsonify({ 'status' : 'running'})

# Define Flask route
@app.route('/predict', methods=['POST'])
def predict_route():
    text = request.json['post']
    prob_lax = predictor_lax(text)
    prob_st = predictor_strict(text)
    return {'status':200,'probability_lax': prob_lax,'probability_strict': prob_st}


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
