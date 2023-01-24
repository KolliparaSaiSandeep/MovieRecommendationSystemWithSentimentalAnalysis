import flask
import io
import string
import time
import os
import numpy as np
import torch
import json
from flask import Flask, jsonify, request,make_response
import transformers
from transformers import BertTokenizer, BertForSequenceClassification
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
def Senti(news):
 finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
 tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
 nlp = transformers.pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)
 results = nlp(news)
 return results[0]['label']


@app.route('/predict', methods=['POST'])
def predict():
  da = request.get_json()
  data = []
  for i in range(len(da)):
      data.append({})
  for i in range(len(da)):
    data[i]["Company"]=da[i]["Company"]
    data[i]["News"]=[{"news":k,"Sentiment":Senti(k)} for k in da[i]["News"]]
  json_data = json.dumps(data)
  return json_data


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.route('/', methods=['GET'])
def index():
    return 'Machine Learning Inference'

@app.route('/pre', methods=['POST'])
def pre():
  da = request.get_json()
  for i in da:
    for j in i.copy():
       i['Sentiment']=Senti(i[j])
  return da

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')