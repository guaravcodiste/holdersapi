from flask import Flask, jsonify
from flask_web3 import current_web3, FlaskWeb3
from flask_cors import CORS, cross_origin
from web3 import Web3
import flask , jsonify,json
from web3.beacon import Beacon

app = flask.Flask(__name__)
cors = CORS(app)
# Set Flask-Web3 configuration

# app.config.update({'ETHEREUM_PROVIDER': 'http', 'ETHEREUM_ENDPOINT_URI': 'https://mainnet.infura.io/v3/edacaf2d3c084ab3abc37bc918f04e03'})


infura_url = "https://rinkeby.infura.io/v3/edacaf2d3c084ab3abc37bc918f04e03"
web3 = Web3(Web3.HTTPProvider(infura_url))
print(web3.isConnected())

# Note : Naming convention need to change
a = web3.eth.get_transaction('0xf4f3a4a0151b49eee84e8c574f253bbeed6bbf6671bad874281b5a9f29d7486b')
b = web3.eth.get_transaction_receipt('0xf4f3a4a0151b49eee84e8c574f253bbeed6bbf6671bad874281b5a9f29d7486b')


abi = json.loads('[	{"inputs": [],"stateMutability": "nonpayable","type": "constructor"},{"inputs": [],"name": "greeting","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"}]')

address = '0xd160B869537760b2BfD2C43E1821Da8607F3D757'

contract = web3.eth.contract(address=web3.toChecksumAddress(address) ,abi=abi)


# print(web3.eth.get_transaction('0xf4f3a4a0151b49eee84e8c574f253bbeed6bbf6671bad874281b5a9f29d7486b'))
##--------------------------------------------------------------------------------------------##

@app.route('/blockNumber',methods=['GET','POST'])
def block_number():
    if flask.request.method == 'GET':
        response_data = {"data":web3.eth.blockNumber,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    elif flask.request.method =='POST':
        response_data = {"data":web3.eth.blockNumber,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400
##--------------------------------------------------------------------------------------------##

@app.route('/balance',methods=['GET','POST'])
def get_balance():
    if flask.request.method == 'GET':
        response_data = {"data":web3.eth.get_balance('0x2fe54D0464a1210620E4594fD7B32a68722aA321'),"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    elif flask.request.method =='POST':
        response_data = {"data":web3.eth.get_balance('0x39C7BC5496f4eaaa1fF75d88E079C22f0519E7b9'),"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200
        
    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400
##--------------------------------------------------------------------------------------------##

@app.route('/currency',methods=['GET','POST'])
def get_currency():
    if flask.request.method == 'GET':
        response_data = {"data":Web3.toWei(5, 'ether'),"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    elif flask.request.method =='POST':
        response_data = {"data":Web3.toWei(5, 'ether'),"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200
        
    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400

##--------------------------------------------------------------------------------------------##
@app.route('/address',methods=['GET','POST'])
def get_address():
    if flask.request.method == 'GET':
        response_data = {"data":Web3.isAddress('0xd3CdA913deB6f67967B99D67aCDFa1712C293601'),"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    elif flask.request.method =='POST':
        response_data = {"data":Web3.isAddress('0xd3CdA913deB6f67967B99D67aCDFa1712C293601'),"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200
        
    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400
##--------------------------------------------------------------------------------------------##
@app.route('/gas',methods=['GET','POST'])
def price_gas():
    if flask.request.method == 'GET':
        response_data = {"data":web3.eth.gas_price,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    elif flask.request.method =='POST':
        response_data = {"data":web3.eth.gas_price ,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200
        
    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400
##--------------------------------------------------------------------------------------------##
@app.route('/hashrate',methods=['GET','POST'])
def hash_rate():
    if flask.request.method == 'GET':
        response_data = {"data":web3.eth.hashrate,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    elif flask.request.method =='POST':
        response_data = {"data":web3.eth.hashrate ,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200
        
    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400
##--------------------------------------------------------------------------------------------##
@app.route('/fee',methods=['GET','POST'])
def max_fee():
    if flask.request.method == 'GET':
        response_data = {"data":web3.eth.max_priority_fee,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    elif flask.request.method =='POST':
        response_data = {"data":web3.eth.max_priority_fee ,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200
        
    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400
##--------------------------------------------------------------------------------------------##
@app.route('/version',methods=['GET','POST'])
def version():
    if flask.request.method == 'GET':
        response_data = {"data":web3.eth.protocol_version,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    elif flask.request.method =='POST':
        response_data = {"data":web3.eth.protocol_version ,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200
        
    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400
##--------------------------------------------------------------------------------------------##

@app.route('/chainid',methods=['GET','POST'])
def chainid():
    if flask.request.method == 'GET':
        response_data = {"data":web3.eth.chain_id,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    elif flask.request.method =='POST':
        response_data = {"data":web3.eth.chain_id ,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200
        
    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400

##--------------------------------------------------------------------------------------------##


@app.route('/transaction_count',methods=['GET','POST'])
def transaction_count():
    if flask.request.method == 'GET':
        response_data = {"data":web3.eth.get_block_transaction_count(4614257) ,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    elif flask.request.method =='POST':
        response_data = {"data":web3.eth.get_block_transaction_count(4187547),"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200
        
    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400
##--------------------------------------------------------------------------------------------##
@app.route('/transaction',methods=['GET','POST'])
def transaction():

    if flask.request.method == 'GET':
        response_data = {"data":(str(a)) ,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    elif flask.request.method =='POST':
        response_data = {"data":(str(a)),"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200
        
    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400

##-----##-----##-----##----##----##----##----##----##-----##----##-----##----##----##----##----##----##---##-----##----##----##-----##
##-----##-----##-----##----##----##----##----##----##-----##----##-----##----##----##----##----##----##---##-----##----##----##-----##
# "data": "AttributeDict({'accessList': [], 
# 'blockHash': HexBytes('0x982c44bffeccf8ab5e194da88956a016067a20646e65d9d5bc176ed89c2a2bc9'),
# 'blockNumber': 9738359,
# 'chainId': '0x4', 
# 'from': '0xa7a82DD06901F29aB14AF63faF3358AD101724A8',
# 'gas': 60000, 
# 'gasPrice': 1000000258, 
# 'hash': HexBytes('0xf4f3a4a0151b49eee84e8c574f253bbeed6bbf6671bad874281b5a9f29d7486b'),
# 'input': '0x', 
# 'maxFeePerGas': 1000000556,
# 'maxPriorityFeePerGas': 1000000000,
# 'nonce': 336795, 
# 'r': HexBytes('0xc0eda0644f5311ef05b477e1dd182d6e7f24cc94092b395f8f6fab610ffc0971'),
# 's': HexBytes('0x2de94d4719e6a620989846e38e6d7f75b37160176b7d477f6446acf2b53b6530'),
# 'to': '0xD46c42553775A0Ec5FF2CFE32bDced325bC7eebF',
# 'transactionIndex': 25,
# 'type': '0x2', 
# 'v': 0, 
# 'value': 100000000000000000})",


@app.route('/transaction_detail',methods=['GET','POST'])
def transaction_gas():

    if flask.request.method == 'GET':
        response_data = {"blockHash":(str(a['blockHash'])) ,"status": True, "message": "Success"}
        block_data = {"blockNumber":(str(a['blockNumber'])) ,"status": True, "message": "Success"}
        chainId_data = {"chainId":(str(a['chainId'])) ,"status": True, "message": "Success"}
        from_data = {"from":(str(a['from'])) ,"status": True, "message": "Success"}
        gas_data = {"gas":(str(a['gas'])) ,"status": True, "message": "Success"}
        gasPrice_data = {"gasPrice":(str(a['gasPrice'])) ,"status": True, "message": "Success"}
        hash_data = {"hash":(str(a['hash'])) ,"status": True, "message": "Success"}
        input_data = {"input":(str(a['input'])) ,"status": True, "message": "Success"}
        maxFeePerGas_data = {"maxFeePerGas":(str(a['maxFeePerGas'])) ,"status": True, "message": "Success"}
        to_data = {"to":(str(a['to'])) ,"status": True, "message": "Success"}
        transactionIndex_data = {"transactionIndex":(str(a['transactionIndex'])) ,"status": True, "message": "Success"}
        type_data = {"type":(str(a['type'])) ,"status": True, "message": "Success"}
        v_data = {"v":(str(a['v'])) ,"status": True, "message": "Success"}
        value_data = {"value":(str(a['value'])) ,"status": True, "message": "Success"}


        

        return flask.jsonify(response_data,block_data,chainId_data,
        from_data,gas_data,gasPrice_data,hash_data,input_data,maxFeePerGas_data,
        to_data,transactionIndex_data,type_data,v_data,value_data), 200
      

    elif flask.request.method =='POST':
        response_data = {"blockHash":(str(a['blockHash'])) ,"status": True, "message": "Success"}
        block_data = {"blockNumber":(str(a['blockNumber'])) ,"status": True, "message": "Success"}
        chainId_data = {"chainId":(str(a['chainId'])) ,"status": True, "message": "Success"}
        from_data = {"from":(str(a['from'])) ,"status": True, "message": "Success"}
        gas_data = {"gas":(str(a['gas'])) ,"status": True, "message": "Success"}
        gasPrice_data = {"gasPrice":(str(a['gasPrice'])) ,"status": True, "message": "Success"}
        hash_data = {"hash":(str(a['hash'])) ,"status": True, "message": "Success"}
        input_data = {"input":(str(a['input'])) ,"status": True, "message": "Success"}
        maxFeePerGas_data = {"maxFeePerGas":(str(a['maxFeePerGas'])) ,"status": True, "message": "Success"}
        to_data = {"to":(str(a['to'])) ,"status": True, "message": "Success"}
        transactionIndex_data = {"transactionIndex":(str(a['transactionIndex'])) ,"status": True, "message": "Success"}
        type_data = {"type":(str(a['type'])) ,"status": True, "message": "Success"}
        v_data = {"v":(str(a['v'])) ,"status": True, "message": "Success"}
        value_data = {"value":(str(a['value'])) ,"status": True, "message": "Success"}


        

        return flask.jsonify(response_data,block_data,chainId_data,
        from_data,gas_data,gasPrice_data,hash_data,input_data,maxFeePerGas_data,
        to_data,transactionIndex_data,type_data,v_data,value_data), 200
        
    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400

##-----##-----##-----##----##----##----##----##----##-----##----##-----##----##----##----##----##----##---##-----##----##----##-----##
##-----##-----##-----##----##----##----##----##----##-----##----##-----##----##----##----##----##----##---##-----##----##----##-----##
# "data": "AttributeDict({'blockHash': HexBytes('0x982c44bffeccf8ab5e194da88956a016067a20646e65d9d5bc176ed89c2a2bc9'),
# 'blockNumber': 9738359, 
# 'contractAddress': None, 
# 'cumulativeGasUsed': 5050393, 
# 'effectiveGasPrice': 1000000258, 
# 'from': '0xa7a82DD06901F29aB14AF63faF3358AD101724A8', 
# 'gasUsed': 21000, 
# 'logs': [], 
# 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'), 
# 'status': 1, 
# 'to': '0xD46c42553775A0Ec5FF2CFE32bDced325bC7eebF', 
# 'transactionHash': HexBytes('0xf4f3a4a0151b49eee84e8c574f253bbeed6bbf6671bad874281b5a9f29d7486b'), 
# 'transactionIndex': 25, 
# 'type': '0x2'})",

@app.route('/transaction_receipt',methods=['GET','POST'])
def transaction_block():


    if flask.request.method == 'GET':
        response_data = {"data":(str(b)) ,"status": True, "message": "Success"}
        block_number_data = {"block_number":(str(b['blockNumber'])) ,"status": True, "message": "Success"}
        contractAddress_data = {"contractAddress":(str(b['contractAddress'])) ,"status": True, "message": "Success"}
        effectiveGasPrice_data = {"effectiveGasPrice":(str(b['effectiveGasPrice'])) ,"status": True, "message": "Success"}
        gasUsed_data = {"gasUsed":(str(b['gasUsed'])) ,"status": True, "message": "Success"}
        logsBloom_data = {"logsBloom":(int(b['logsBloom'])) ,"status": True, "message": "Success"}
        status_data = {"status":(str(b['status'])) ,"status": True, "message": "Success"}

        return flask.jsonify(response_data,block_number_data,contractAddress_data,effectiveGasPrice_data,effectiveGasPrice_data,
        gasUsed_data,logsBloom_data,status_data), 200

    elif flask.request.method =='POST':
        response_data = {"data":(str(b)) ,"status": True, "message": "Success"}
        block_number_data = {"block_number":(str(b['blockNumber'])) ,"status": True, "message": "Success"}
        contractAddress_data = {"contractAddress":(str(b['contractAddress'])) ,"status": True, "message": "Success"}
        effectiveGasPrice_data = {"effectiveGasPrice":(str(b['effectiveGasPrice'])) ,"status": True, "message": "Success"}
        gasUsed_data = {"gasUsed":(str(b['gasUsed'])) ,"status": True, "message": "Success"}
        logsBloom_data = {"logsBloom":(str(b['logsBloom'])) ,"status": True, "message": "Success"}
        status_data = {"status":(str(b['status'])) ,"status": True, "message": "Success"}

        return flask.jsonify(response_data,block_number_data,contractAddress_data,effectiveGasPrice_data,effectiveGasPrice_data,
        gasUsed_data,logsBloom_data,status_data), 200
        
    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400

##-----##-----##-----##----##----##----##----##----##-----##----##-----##----##----##----##----##----##---##-----##----##----##-----##
##-----##-----##-----##----##----##----##----##----##-----##----##-----##----##----##----##----##----##---##-----##----##----##-----##

@app.route('/count',methods=['GET','POST'])
def count():

    if flask.request.method == 'GET':
        response_data = {"data":web3.eth.get_transaction_count('0xa7a82dd06901f29ab14af63faf3358ad101724a8') ,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    elif flask.request.method =='POST':
        response_data = {"data":(str(a)),"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200
        
    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400

##-----##-----##-----##----##----##----##----##----##-----##----##-----##----##----##----##----##----##---##-----##----##----##-----##

@app.route('/proof',methods=['GET','POST'])
def proof():

    if flask.request.method == 'GET':
        response_data = {"data":web3.eth.syncing,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    elif flask.request.method =='POST':
        response_data = {"data":web3.eth.hashrate,"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200
        
    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400

##-----##-----##-----##----##----##----##----##----##-----##----##-----##----##----##----##----##----##---##-----##----##----##-----##
##-----##-----##-----##----##----##----##----##----##-----##--Eth 2.0 Beacon API--##-----##----##----##----##----##----##---##-----##----##----##-----##
##-----##-----##-----##----##----##----##----##----##-----##----##-----##----##----##----##----##----##---##-----##----##----##-----##


@app.route('/getblock',methods=['GET','POST'])
def get_block():

    if flask.request.method == 'GET':
        response_data = {"data":Beacon.get_finality_checkpoint(state_id="head"),"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    elif flask.request.method =='POST':
        response_data = {"data":web3.eth.get_block(9743048),"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200
        
    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400

##-----##-----##-----##----##----##----##----##----##-----##----##-----##----##----##----##----##----##---##-----##----##----##-----##
infura = "https://ropsten.infura.io/v3/edacaf2d3c084ab3abc37bc918f04e03"
peb3 = Web3(Web3.HTTPProvider(infura))

abi = json.loads('[	{"inputs": [],"stateMutability": "nonpayable","type": "constructor"},{"inputs": [],"name": "greeting","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"}]')

address = '0x43941f8fe00EF6CE2Aff3B6Aa330E2e7861e245D'
# 0xd160B869537760b2BfD2C43E1821Da8607F3D757
contract = peb3.eth.contract(address=peb3.toChecksumAddress(address) ,abi=abi)

@app.route('/',methods=['GET','POST'])
def greeth():

    if flask.request.method == 'GET':
        response_data = {"data":contract.functions.greeting().call(),"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    elif flask.request.method =='POST':
        response_data = {"data":contract.functions.greeting().call(),"status": True, "message": "Success"}
        return flask.jsonify(response_data), 200
        
    else:
        response_data = {"status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400

# print(contract.functions.greeting().call())

##-----##-----##-----##----##----##----##----##----##-----##----##-----##----##----##----##----##----##---##-----##----##----##-----##


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888,debug=True)

