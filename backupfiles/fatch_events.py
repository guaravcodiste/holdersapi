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

def main():
    infura_url = "https://bsc-dataseed1.binance.org"
    web3 = Web3(Web3.HTTPProvider(infura_url))
    print(web3.isConnected())

    # # with open('/home/codiste/projects/api/blockchain/semple/UniswapV2Pair.json', 'r') as f:
    # #   abi = json.loads(f.read())

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
    print(colored(latest_blocks,'cyan'))

    transferEvents = contract.events.Transfer.createFilter(fromBlock=latest_blocks-5, toBlock=latest_blocks)
    print(colored(len(transferEvents.get_all_entries()),'yellow'))
    event_len = len(transferEvents.get_all_entries())

    data_event = transferEvents.get_all_entries()
    # print(data_event)
    try:
        for i in data_event:
            insertData(i)
        print(f"{event_len}=>Data Inserted in the table ")
    except:
        print(colored("Data Not Inserted in the table",'red'))

    # From_address = (data_event[0]['args']['from'])
    # To_address = (data_event[0]['args']['to'])
    # value = (data_event[0]['args']['value'])
    # Block_number = (data_event[0]['blockNumber'])

    # print(colored(From_address,'cyan'))
    # print(colored(To_address,'green'))
    # print(colored(value,'yellow'))
    # print(colored(Block_number,'cyan'))


  

def insertData(data):
        con = sqlite3.connect('TransferEvents.db')
        currentDateTime = datetime.datetime.now()
        cur = con.cursor()

            # Create table
        # table = '''CREATE TABLE firstevent
        #            (fromAddress VARCHAR(255), toAddress VARCHAR(255),value VARCHAR(255),BlockNumber VARCHAR(225),SubmissionDate TIMESTAMP);'''
        # cur.execute(table)
        
            #insert record
        cur.execute(f'''INSERT INTO firstevent VALUES ('{data['args']['from']}', '{data['args']['to']}', '{data['args']['value']}','{data['blockNumber']}','{currentDateTime}')''')



        try:
            statement = '''SELECT * FROM firstevent ORDER BY Blocknumber DESC LIMIT 1'''
            cur.execute(statement)
            output = cur.fetchone()
            print(output["BlockNumber"])
        except:
            print("select query not work")



        con.commit()
        con.close()

if __name__ == "__main__":
 print (colored("Script has started...",'green'))
 main()
 print (colored("Script has Ended...",'green'))