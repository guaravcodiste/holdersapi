from retrying import retry
import json
import re
import flask
from flask_cors import CORS, cross_origin
from termcolor import colored
from web3 import Web3
import sqlite3
import datetime


app = flask.Flask(__name__)

##--------------------------------------Network-And-Address-Connection------------------------------------------------##
infura_url = "https://bsc-dataseed1.binance.org"
# infura_url = "https://data-seed-prebsc-1-s1.binance.org:8545/"
web3 = Web3(Web3.HTTPProvider(infura_url))
connection = web3.isConnected()
print(colored(f"web3 connection is: {connection}",'green'))

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


 
def fetchData(dbPath, blockNumber):

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

def currentBalance(blockNumber):
    rows = fetchData("./TransferEventsData.db", blockNumber)

    holdings = {}
    for row in rows:
        fromAddress = row[0]
        toAddress = row[1]
        value = row[2]

        if fromAddress not in holdings.keys():
            holdings[fromAddress] = 0

        if toAddress not in holdings.keys():
            holdings[toAddress] = 0

        holdings[fromAddress] -= value
        if holdings[fromAddress] < 0:
            holdings[fromAddress] = 0
        holdings[toAddress] += value

    print (colored("Script has Ended...",'green'))
    response_data = {"Balance":holdings, "status": True, "message": "Get Current Balance Successfully"}
    return flask.jsonify(response_data), 200
##---------------------------------------Function----------------------------------------------##
def TransferEvent(Database_last_block,toBlock1):
    print(colored(f"{Database_last_block} To {toBlock1} ",'yellow'))
    transferEvents = contract.events.Transfer.createFilter(fromBlock= Database_last_block , toBlock = toBlock1)
    data_event = transferEvents.get_all_entries()
    return data_event  

def UpdateDatabase(latest_block):
    latest_blocks = latest_block
    con = sqlite3.connect('firstTime.db')
    cur = con.cursor()
    sql_query_table = """SELECT name FROM sqlite_master  
    WHERE type='table' and name='firstevent';"""
    cur.execute(sql_query_table)
    all_table = cur.fetchone()

    ###------------Check database ------------##
  
    if all_table == None:
        print(colored("if condition...",'red'))
        con = sqlite3.connect('firstTime.db')
        cur = con.cursor()
            # Create table
        Newtable = '''CREATE TABLE firstevent
                   (fromAddress VARCHAR(255), toAddress VARCHAR(255),value INT(255),transactionHash VARCHAE(225),
                   BlockNumber INT(225),Date TIMESTAMP,UNIQUE (fromAddress,toAddress,transactionHash) ON CONFLICT IGNORE);'''
        cur.execute(Newtable)
        con.commit()
        con.close()
        print("Database and table create....")
        FirstBolck = 176416
        # transferEvents = contract.events.Transfer.createFilter(fromBlock= FirstBolck , toBlock = FirstBolck+1000)
        # data_event = transferEvents.get_all_entries()

        # try:
        #     for i in data_event:
        #         insertData(i)
        #     print (colored("Script has Ended...",'green'))
        #     response_data = {"data":{}, "status": True, "message": "Data Inserted Successfully"}
        #     return flask.jsonify(response_data), 200

        # except:
        #     response_data = {"data": {}, "status": False, "message": "Data Not Inserted in the Database Table"}
        #     return flask.jsonify(response_data), 400
        BlockLimit = 5000           
        toBlock1 = FirstBolck + BlockLimit
        for j in range(FirstBolck,latest_blocks,BlockLimit):
            if FirstBolck != j:
                    FirstBolck = toBlock1 + 1
                    toBlock1 = toBlock1 + BlockLimit

            try:
                isScuuess = TransferEvent(FirstBolck,toBlock1)
                print(colored("try... To Updateing Data",'cyan'))
                if isScuuess != None:
                    insertrecord(isScuuess)
            except Exception as e:
                    isScuuess = None
                    while e and isScuuess is None:
                        try:
                            print(colored(f"{FirstBolck} To {toBlock1} : Retry... ",'red'))
                            isScuuess = TransferEvent(FirstBolck,toBlock1)
                            print(colored("try... To Updateing Data",'cyan'))
                            if isScuuess != None:
                                insertrecord(isScuuess)
                        except:
                            pass

        response_data = {"data": {}, "status": False, "message": "Data Not Inserted in the Database Table"}
        return flask.jsonify(response_data), 400
        
 
    else:
        print(colored("else condition...",'red'))
        statement = '''SELECT * FROM firstevent ORDER BY Blocknumber DESC LIMIT 1'''
        cur.execute(statement)
        block = cur.fetchone()
        Database_last_block = int(block[4])
        print(colored(f"Latest Block : {latest_blocks}",'cyan'))
        print(colored(f"Database Last Block : {Database_last_block}",'cyan'))
        con.commit()
        con.close()

        ##-------------Limit up to 5000------------------------------##
        # def TransferEvent(Database_last_block,toBlock1):
        #     print(colored(f"{Database_last_block} To {toBlock1} ",'yellow'))
        #     transferEvents = contract.events.Transfer.createFilter(fromBlock= Database_last_block , toBlock = toBlock1)
        #     data_event = transferEvents.get_all_entries()
        #     return data_event      


        BlockLimit = 5000           
        toBlock1 = Database_last_block + BlockLimit
        for j in range(Database_last_block,latest_blocks,BlockLimit):
            if Database_last_block != j:
                    Database_last_block = toBlock1 + 1
                    toBlock1 = toBlock1 + BlockLimit

            try:
                isScuuess = TransferEvent(Database_last_block,toBlock1)
                print(colored("try... To Updateing Data",'cyan'))
                if isScuuess != None:
                    insertrecord(isScuuess)
            except Exception as e:
                    isScuuess = None
                    while e and isScuuess is None:
                        try:
                            print(colored(f"{Database_last_block} To {toBlock1} : Retry... ",'red'))
                            isScuuess = TransferEvent(Database_last_block,toBlock1)
                            print(colored("try... To Updateing Data",'cyan'))
                            if isScuuess != None:
                                insertrecord(isScuuess)
                        except:
                            pass

        response_data = {"data": {}, "status": False, "message": "Data Not Inserted in the Database Table"}
        return flask.jsonify(response_data), 400
               
def insertrecord(newData):
    try:
        for i in newData:
            insertData(i)
        print (colored("Data update Successfully...",'green'))
        response_data = {"data":{}, "status": True, "message": "Data Inserted Successfully"}
        return flask.jsonify(response_data), 200

    except:
        response_data = {"data": {}, "status": False, "message": "Data Not Inserted in the Database Table"}
        return flask.jsonify(response_data), 400



def insertData(data):
    con = sqlite3.connect('firstTime.db')
    currentDateTime = datetime.datetime.now()
    cur = con.cursor()
    Hash = (data['transactionHash'].hex())
    cur.execute(f'''INSERT INTO firstevent VALUES ('{data['args']['from']}', '{data['args']['to']}', '{data['args']['value']}','{Hash}','{data['blockNumber']}','{currentDateTime}')''')

    con.commit()
    con.close()


##----------------------------------------Api-Route------------------------------------------------##
@app.route('/UpdateDatabase',methods=['POST'])
@cross_origin()
def token():      
    if flask.request.method == 'POST':
        print (colored("Updating Database...",'green'))
        latest_block = web3.eth.block_number
        response_data = UpdateDatabase(latest_block)
        return response_data
    else:
        response_data = {"data": {}, "status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400

@app.route('/currentBalance',methods=['POST'])
@cross_origin()
def getbalance():      
    if flask.request.method == 'POST':
        print (colored("Fetching Current Balance...",'green'))
        blockNumber = flask.request.json
        response_data = currentBalance(blockNumber)
        return response_data
    else:
        response_data = {"data": {}, "status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400

if __name__ == "__main__":
 app.run(host="0.0.0.0", port=4000,debug=True)

