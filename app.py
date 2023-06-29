import json, config
from flask import Flask, request, jsonify, render_template
from kucoin.client import Client
import os
import requests
import time
import hashlib
import hmac
import base64


api_host = 'https://api.kucoin.com'


app = Flask(__name__)


client = Client(config.API_KEY, config.API_SECRET, config.API_PASSPHRASE)


@app.route("/")
def index():
    return "Hello World!"

@app.route('/webhook', methods=['POST'])
def webhook():
    #print(request.data)

    data = json.loads(request.data)
    if data['passphrase'] != config.TV_WEBHOOK:
        print("faallasteeee") 

    side = data['strategy']['order_action'] 
    url = "https://api.kucoin.com/api/v1/orders"
    now = int(time.time() * 1000)
    data = {"clientOid": "ABB", "side": side, "symbol": "BTC-USDT", "type": "market", "size": "0.0001"}
    data_json = json.dumps(data)
    str_to_sign = str(now) + 'POST' + '/api/v1/orders' + data_json

    signature = base64.b64encode(hmac.new(config.API_SECRET.encode(
            'utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(config.API_SECRET.encode(
            'utf-8'), config.API_PASSPHRASE.encode('utf-8'), hashlib.sha256).digest())

    headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": config.API_KEY,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2",
            "Content-Type": "application/json"
    }

    try:
            res = requests.post(
                url, headers=headers, data=data_json).json()

            print(res)

    except Exception as err:
            print(err)

    if res:
        return {
            "code": "success",
            "message": "order executed"
        }
    else:
        print("order failed")
        return {
            "code": "error",
            "message": "order failed"
        }

@app.route('/webhook10', methods=['POST'])
def webhook10():
    #print(request.data)

    data = json.loads(request.data)
    if data['passphrase'] != config.TV_WEBHOOK:
        print("faallasteeee") 

    side = data['strategy']['order_action'] 
    url = "https://api.kucoin.com/api/v1/margin/order"
    now = int(time.time() * 1000)
    data = {"clientOid": "BBB", "side": side, "symbol": "BTC-USDT", "type": "market", "size": "0.002", "tradeType": "MARGIN_TRADE"}
    data_json = json.dumps(data)
    str_to_sign = str(now) + 'POST' + '/api/v1/margin/order' + data_json

    signature = base64.b64encode(hmac.new(config.API_SECRET.encode(
            'utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(config.API_SECRET.encode(
            'utf-8'), config.API_PASSPHRASE.encode('utf-8'), hashlib.sha256).digest())

    headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": config.API_KEY,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2",
            "Content-Type": "application/json"
    }

    try:
            res = requests.post(
                url, headers=headers, data=data_json).json()

            print(res)

    except Exception as err:
            print(err)

    if res:
        return {
            "code": "success",
            "message": "order executed"
        }
    else:
        print("order failed")
        return {
            "code": "error",
            "message": "order failed"
        }
