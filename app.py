import json, config
from flask import Flask, request, jsonify, render_template
from kucoin.client import Client
import os
api_key = os.environ['API_KEY']
api_secret = os.environ['API_SECRET']
api_passphrase = os.environ['API_PASSPHRASE']
api_host = 'https://api.kucoin.com'
import requests
import time
import hashlib
import hmac
import base64
#from binance.client import Client
#from binance.enums import *

app = Flask(__name__)

#client = Client(config.API_KEY, config.API_SECRET, tld='us')
client = Client(config.API_KEY, config.API_SECRET, api_passphrase)

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

    #side = data['strategy']['order_action'].upper()
    #quantity = data['strategy']['order_contracts']
    #order_response = order(side, quantity, "DOGEUSD")




def test_post_order():
    host = api_host
    key = api_key
    passphrase = api_passphrase

    endpoint = '/api/v1/orders'
    body = '{"side":"buy","symbol":"BTC-USDT","type":"market","size":"2","clientOid":"' + str(time.time()) + '"}'

    timestamp = int(time.time() * 1000)

    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['KC-API-KEY'] = key
    headers['KC-API-TIMESTAMP'] = str(timestamp)
    headers['KC-API-PASSPHRASE'] = passphrase
    headers['KC-API-SIGN'] = signature(endpoint, body, timestamp, 'POST')

    request_path = host + endpoint

    response = requests.post(request_path, headers=headers, data=body)

    print(response.json())

def signature(endpoint, body, timestamp, method):
    secret = api_secret
    message = str(timestamp) + method + endpoint + body
    hmac_key = base64.b64decode(secret)
    signature = hmac.new(hmac_key, message.encode('utf-8'), hashlib.sha256)
    return base64.b64encode(signature.digest())

test_post_order()


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

        ########
        #import asyncio
#from kucoin.client import Clientfrom kucoin.asyncio import KucoinSocketManager
#api_key = '<api_key>'api_secret = '<api_secret>'api_passphrase = '<api_passphrase>'
#
#async def get_kucoin_data():    global loop
    ## callback function that receives messages from the socket    async def handle_evt(msg):        if msg['topic'] == '/market/ticker:ETH-USDT':            print(f'got ETH-USDT tick:{msg["data"]}')
    #client = Client(api_key, api_secret, api_passphrase)
    #ksm = await KucoinSocketManager.create(loop, client, handle_evt)
    #await ksm.subscribe('/market/ticker:ETH-USDT')
    #while True:        print("sleeping to keep loop open")        await asyncio.sleep(20, loop=loop)
#
#await(get_kucoin_data())