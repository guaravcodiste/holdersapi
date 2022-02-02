from flask import Flask, render_template, request, url_for, redirect
from flask_web3 import current_web3, FlaskWeb3
from flask_cors import CORS, cross_origin
from web3 import Web3, HTTPProvider
import flask , jsonify,json
from flask_cors import CORS, cross_origin
from termcolor import colored
import requests


app = flask.Flask(__name__)
cors = CORS(app)
# -------------------Token-Api-----------------------
# curl -X 'GET' \
#   'https://public-api.solscan.io/account/tokens?account=CuieVDEDtLo7FypA9SbLM9saXFdb1dsshEkyErMqkRQq' \
#   -H 'accept: application/json'

headers = {
    'Content-type':'application/json', 
    'Accept':'application/json' 
}
url_token = 'https://public-api.solscan.io/account/tokens?account=2qzTURMGo9gVdwYyCbyiTrvyDCvLNDaRPkiWefdnmExb'

token_data = requests.get(url_token,headers=headers)
token = token_data.json()
Token = {}
if  len(token) > 0:
    tokenArr = token
    for x in  tokenArr:
        name = "None"
        if (x['tokenName']):
            name = (x['tokenName'])
        balance = "None"
        if (x['tokenAmount']['amount']):
            balance = (x['tokenAmount']['amount'])
        Token[str(name)]=int(balance)
        print(name)
        print(balance)
    print(Token)   


# -----------------------Balance-------------------------------------
# curl http://localhost:8899 -X POST -H "Content-Type: application/json" -d '
#   {"jsonrpc":"2.0", "id":1, "method":"getBalance", "params":["83astBRguLMdt2h5U1Tpdq5tjFoJ6noeGwaY3mDLVcri"]}
# '
Lamport = 1000000000
headers = {
    'Content-type':'application/json', 
    'Accept':'application/json' 
}
url = 'https://api.testnet.solana.com'
data = {"jsonrpc":"2.0", "id":1, "method":"getBalance", "params":["4ETf86tK7b4W72f27kNLJLgRWi9UfJjgH4koHGUXMFtn"]}
# {'jsonrpc': '2.0', 'result': {'context': {'slot': 111471580}, 'value': 17000000150}, 'id': 1}
# 69847276318434525
my_data = requests.post(url,json=data, headers=headers)
solona = my_data.json()
# solona_balance = solona['result']['value']
solona_balance = solona['result']['value'] / Lamport
print (colored(solona_balance,'green'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)

