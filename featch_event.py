from cgi import print_environ
from xml.dom import NoModificationAllowedErr
import flask
from flask_cors import CORS, cross_origin
from termcolor import colored
from web3 import Web3
import sqlite3
import datetime
app = flask.Flask(__name__)

##--------------------------------------Network-And-Address-Connection------------------------------------------------##
infura_url = "https://bsc-dataseed1.binance.org"
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
FirstBolck = 176416
BlockLimit = 5000           

 ##-------------------------------------Get-currentBalance-Function----------------------------------------------##

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
    rows = fetchData("./TransferEvents.db", blockNumber)

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
##--------------------------------------UpdateDatabase-Function----------------------------------------------##
def TransferEvent(Database_last_block,toBlock1):
    print(colored(f"Block :{Database_last_block} To {toBlock1} ",'yellow'))
    transferEvents = contract.events.Transfer.createFilter(fromBlock= Database_last_block , toBlock = toBlock1)
    data_event = transferEvents.get_all_entries()
    return data_event  

def getLastBlock():
    try:
        con = sqlite3.connect('TransferEvents.db')
        cur = con.cursor()  
        statement = '''SELECT * FROM firstevent ORDER BY Blocknumber DESC LIMIT 1'''
        cur.execute(statement)
        block = cur.fetchone()
        Database_last_block = int(block[4])

        return Database_last_block
    except:
        return FirstBolck

def UpdateDatabase(latest_blocks):
    con = sqlite3.connect('TransferEvents.db')
    cur = con.cursor()
    cur.execute ('''CREATE TABLE IF NOT EXISTS firstevent (fromAddress VARCHAR(255), toAddress VARCHAR(255),value INT(255),transactionHash VARCHAE(225),
                    BlockNumber INT(225),Date TIMESTAMP,UNIQUE (fromAddress,toAddress,transactionHash) ON CONFLICT IGNORE);''')
    
    con.commit()
    con.close()

    lastBLock = getLastBlock()
    print(colored(f"From Block : {lastBLock}",'cyan'))
    print(colored(f"Latest Block : {latest_blocks}",'cyan'))
    
    ##-------------Limit up to 5000------------------------------##
    
    for j in range(lastBLock,latest_blocks,BlockLimit):
        if j+BlockLimit > latest_blocks:
            response_data = {"data": {}, "status": False, "message": "Retry After Sometime..."}
            return flask.jsonify(response_data), 400
        else:
            # Retry Logic 
            fail = True
            while(fail):
                try:
                    events = TransferEvent(j, j+BlockLimit)
                    print(colored("try... To Updateing Database",'cyan'))
                    if events:
                        insertData(events)
                    fail = False
                except:
                    print(colored(f"Block :{j} To {j+BlockLimit} Retry...",'red'))
                    pass     

def insertData(newData):
    con = sqlite3.connect('TransferEvents.db')
    currentDateTime = datetime.datetime.now()
    cur = con.cursor()
    for data in newData:
        Hash = (data['transactionHash'].hex())
        cur.execute(f'''INSERT OR IGNORE INTO firstevent VALUES ('{data['args']['from']}', '{data['args']['to']}', '{data['args']['value']}','{Hash}','{data['blockNumber']}','{currentDateTime}')''')
    print(colored("Database Update Successfully...",'green'))
    con.commit()
    con.close()

##----------------------------------------Api-Route------------------------------------------------##
@app.route('/UpdateDatabase',methods=['POST'])
@cross_origin()
def token():      
    if flask.request.method == 'POST':
        print (colored("Updating Database...",'green'))
        latest_blocks = web3.eth.block_number
        response_data = UpdateDatabase(latest_blocks)
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
