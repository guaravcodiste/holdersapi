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

# lastBlock = 14322570


##---------------------------------------Function--------------------------------------------------##

def main():
    ##---------------------------Database-To-Get-Last-Blocknumber-------------------------------##
    con = sqlite3.connect('TransferEventData.db')
    currentDateTime = datetime.datetime.now()
    cur = con.cursor()

    # table = '''CREATE TABLE firstevent
    #             (fromAddress VARCHAR(255), toAddress VARCHAR(255),value VARCHAR(255),BlockNumber VARCHAR(225),Date TIMESTAMP);'''
    # cur.execute(table)

    try:
        statement = '''SELECT * FROM firstevent ORDER BY Blocknumber DESC LIMIT 1'''
        cur.execute(statement)
        block = cur.fetchone()
        last_block = int(block[3])
        print(colored(f"Database Last Block : {last_block}",'cyan'))
    except:
        print("No data Found...")
    con.commit()
    con.close()
    ##--------------------------------------END---------------------------------------------------##

    transferEvents = contract.events.Transfer.createFilter(fromBlock=last_block, toBlock=last_block+100)
    event_len = len(transferEvents.get_all_entries())

    data_event = transferEvents.get_all_entries()
    # print(data_event)
    try:
        for i in data_event:
            insertData(i)
        print (colored(f"{event_len}=>Data Inserted in the Database Table ",'yellow'))
        print (colored("Script has Ended...",'green'))
        return "success"
    except:
        print (colored("Data Not Inserted in the Database Table",'red'))
        return "faild"
  

def insertData(data):
        con = sqlite3.connect('TransferEventData.db')
        currentDateTime = datetime.datetime.now()
        cur = con.cursor()

            # Create table
        # table = '''CREATE TABLE firstevent
        #            (fromAddress VARCHAR(255), toAddress VARCHAR(255),value VARCHAR(255),BlockNumber VARCHAR(225),Date TIMESTAMP);'''
        # cur.execute(table)
        
            #insert record
        cur.execute(f'''INSERT INTO firstevent VALUES ('{data['args']['from']}', '{data['args']['to']}', '{data['args']['value']}','{data['blockNumber']}','{currentDateTime}')''')

        con.commit()
        con.close()


##----------------------------------------Api-Route------------------------------------------------##
@app.route('/',methods=['GET', 'POST'])
@cross_origin()
def token():      
  
    if flask.request.method == 'GET':
        return "Hello!!"
    elif flask.request.method == 'POST':
        print (colored("Script has started...",'green'))
        response_data =main()
        return response_data
    else:
        response_data = {"data": {}, "status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400

if __name__ == "__main__":
 app.run(host="0.0.0.0", port=4000,debug=True)