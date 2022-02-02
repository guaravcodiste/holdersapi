from flask import Flask, render_template, request, url_for, redirect
from flask_web3 import current_web3, FlaskWeb3
from flask_cors import CORS, cross_origin
from web3 import Web3, HTTPProvider
import flask , jsonify,json
from web3.beacon import Beacon
from flask_cors import CORS, cross_origin
from termcolor import colored
import requests


app = flask.Flask(__name__)
cors = CORS(app)

# curl -X 'GET' \
#   'https://testnet-algorand.api.purestake.io/idx2/v2/accounts/GW6T5RAUWG5H6A4LP7UWL2PYGAZJUL6RCBWSU24PO27COCT3MMS6YCU2Z4' \
#   -H 'accept: application/json' \
#   -H 'x-api-key: r1hPXdqrtl3SjSh1LICs45wIjm7JB8p1TyFXMHEg'

Lamport = 1000000
headers = {
    'x-api-key': 'r1hPXdqrtl3SjSh1LICs45wIjm7JB8p1TyFXMHEg', 
    'Accept':'application/json' 
}
url = 'https://mainnet-algorand.api.purestake.io/idx2/v2/accounts/GW6T5RAUWG5H6A4LP7UWL2PYGAZJUL6RCBWSU24PO27COCT3MMS6YCU2Z4'
my_data = requests.get(url,headers=headers)
algod = my_data.json()

algod_balance = algod['account']['amount']/ Lamport
print (colored(algod_balance,'green'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)

