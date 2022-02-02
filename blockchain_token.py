import os
import json
import flask
import requests
from flask_cors import CORS, cross_origin
from termcolor import colored
from operator import itemgetter
from web3 import Web3, HTTPProvider

app = flask.Flask(__name__)





Lamport = 1000000000000000000
def data(par):
    address = par['address']
    urls = {
        "Ethereum": f"https://api.covalenthq.com/v1/42/address/{address}/balances_v2/?quote-currency=USD&format=JSON&nft=false&no-nft-fetch=false&key=ckey_373f6fe9f142487689b67de0e72",
        "Binance": f"https://api.covalenthq.com/v1/97/address/{address}/balances_v2/?quote-currency=USD&format=JSON&nft=false&no-nft-fetch=false&key=ckey_373f6fe9f142487689b67de0e72",
        "Polygon_MATIC" : f"https://api.covalenthq.com/v1/80001/address/{address}/balances_v2/?quote-currency=USD&format=JSON&nft=false&no-nft-fetch=false&key=ckey_373f6fe9f142487689b67de0e72",
        "Fantom_FTM" : f"https://api.covalenthq.com/v1/4002/address/{address}/balances_v2/?quote-currency=USD&format=JSON&nft=false&no-nft-fetch=false&key=ckey_373f6fe9f142487689b67de0e72",
        "Hecoinfo_HT" : f"https://api.covalenthq.com/v1/256/address/{address}/balances_v2/?quote-currency=USD&format=JSON&nft=false&no-nft-fetch=false&key=ckey_373f6fe9f142487689b67de0e72"
    }
    mainObj = {}
    for i in urls:
        responce = getTokenData(urls[i])
        mainObj[i] = responce
    ether_token =mainObj['Ethereum']
    print(ether_token)
    ether_token =mainObj['Binance']
    print(ether_token)
    ether_token =mainObj['Polygon_MATIC']
    print(ether_token)
    ether_token =mainObj['Fantom_FTM']
    print(ether_token)
    ether_token =mainObj['Hecoinfo_HT']
    print(ether_token)
    return mainObj
# ####-----------------------------------------####

def getTokenData(url):
        # print(url)
        tokenData = requests.get(url)
        # print(tokenData.json())
        Token = {}
        jsontokenData = tokenData.json()

        if  len(jsontokenData) > 0:
            tokenArr = jsontokenData['data']['items']
            for x in  tokenArr:
                name = (x["contract_name"])
                balance = (x["balance"])
                Token[str(name)]=int(balance)
            print(Token)   
            return Token

@app.route('/token',methods=['GET', 'POST'])
@cross_origin()
def token_():      
  
    if flask.request.method == 'GET':
        return "Hello!!"
    elif flask.request.method == 'POST':
        par = flask.request.json
        print(colored(par, "cyan"))
        response_data =data(par)
        return response_data
    else:
        response_data = {"data": {}, "status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000,debug=True)
# {
#     "quote-currency":"USD",
#     "format" : "JSON",
#     "nft" : "false",
#     "no-nft-fetch": "false",
#     "key" : "ckey_373f6fe9f142487689b67de0e72"

# }