import os
import json
import flask
import requests
from flask_cors import CORS, cross_origin
from termcolor import colored
from operator import itemgetter
from web3 import Web3, HTTPProvider
import time
import sqlite3
import datetime

app = flask.Flask(__name__)

##--------------------------------------Network-And-Address-Connection------------------------------------------------##
infura_url = "https://bsc-dataseed1.binance.org"
# infura_url = "https://data-seed-prebsc-1-s1.binance.org:8545/"
web3 = Web3(Web3.HTTPProvider(infura_url))
print(web3.isConnected())

abi = [
    {
        "anonymous": False,
        "inputs": [
        {
            "indexed": True,
            "internalType": "address",
            "name": "from",
            "type": "address"
        },
        {
            "indexed": True,
            "internalType": "address",
            "name": "to",
            "type": "address"
        },
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "value",
            "type": "uint256"
        }
        ],
        "name": "Transfer",
        "type": "event"
    },
]

address='0x55d398326f99059fF775485246999027B3197955'
contract = web3.eth.contract(address=web3.toChecksumAddress(address) ,abi=abi)

latest_blocks = web3.eth.block_number
print(colored(f"Latest Block : {latest_blocks}",'cyan'))

# lastBlock = 176416


def fetchData(dbPath, blockNumber):
    if flask.request.method == 'POST':
            blockNumber = blockNumber['Bolcknumber']
            print(colored(blockNumber,'green'))

            con = sqlite3.connect(dbPath)
            cur = con.cursor()

            fetchQuery = f'''SELECT * FROM firstevent WHERE BlockNumber <= {blockNumber} ORDER BY BlockNumber ASC'''
            cur.execute(fetchQuery)
            rows = cur.fetchall()

            con.commit()
            con.close()
            return rows

def main(blockNumber):
        if flask.request.method == 'POST':
            # blockNumber = blockNumber['Bolcknumber']
            rows = fetchData("./TransferEventData.db", blockNumber)

            holdings = {
                "abhi": 100
            }

            for row in rows:
                fromAddress = row[0]
                toAddress = row[1]
                value = row[2]

                if fromAddress not in holdings.keys():
                    holdings[fromAddress] = 0

                if toAddress not in holdings.keys():
                    holdings[toAddress] = 0

                holdings[fromAddress] -= value
                holdings[toAddress] += value

            # print(holdings)
            json_object = json.dumps(holdings, indent = 4) 
            # print(json_object)
            return json_object
        # main(14554827)


##----------------------------------------Api-Route------------------------------------------------##

@app.route('/currentbalance',methods=['GET', 'POST'])
@cross_origin()
def getbalance():      
  
    if flask.request.method == 'GET':
        return "Hello!!"
    elif flask.request.method == 'POST':
        print (colored("Script has started...",'green'))
        blockNumber = flask.request.json
        print(colored(blockNumber,'red'))
        response = main(blockNumber)
        return response
    else:
        response_data = {"data": {}, "status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400

if __name__ == "__main__":
 app.run(host="0.0.0.0", port=4000,debug=True)