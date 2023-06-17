import json, config
from flask import Flask, request, jsonify, render_template
from kucoin.client import Client
import os
api_key = os.environ['648a281c5ebac60001ea3cf3']
api_secret = os.environ['090053cb-827d-4919-8ab6-ed357e43230e']
api_passphrase = os.environ['ApiApi123']

#from binance.client import Client
#from binance.enums import *

app = Flask(__name__)

#client = Client(config.API_KEY, config.API_SECRET, tld='us')
client = Client(api_key, api_secret, api_passphrase)

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    #print(request.data)
    data = json.loads(request.data)
    
    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }

    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']
    order_response = order(side, quantity, "DOGEUSD")

    if order_response:
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