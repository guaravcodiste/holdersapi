from flask import Flask, render_template, request, url_for, redirect
from flask_web3 import current_web3, FlaskWeb3
from flask_cors import CORS, cross_origin
from web3 import Web3, HTTPProvider
import flask , jsonify,json
# from web3.beacon import Beacon
from flask_cors import CORS, cross_origin
from termcolor import colored
import requests


app = flask.Flask(__name__)
cors = CORS(app)


##-------------------trsting address-----------------------------##
# 0xD62856a1faF77Ee5fFA85dDeCbD4462e1A52CA4F

##--------------------------- URL -------------------------------------------##

infura_url = "https://kovan.infura.io/v3/edacaf2d3c084ab3abc37bc918f04e03"
Ether= Web3(Web3.HTTPProvider(infura_url))
print(Ether.isConnected())

rpc_url = "https://data-seed-prebsc-1-s1.binance.org:8545/"
BNB = Web3(Web3.HTTPProvider(rpc_url))
print(BNB.isConnected())

rpc_url2 = "https://rpc-mumbai.maticvigil.com/"
polygon = Web3(Web3.HTTPProvider(rpc_url2))
print(polygon.isConnected())

rpc_url3 = "https://rpc.testnet.fantom.network/"
Fantom = Web3(Web3.HTTPProvider(rpc_url3))
print(Fantom.isConnected())

rpc_url4 = "https://http-testnet.hecochain.com/"
Hecoinfo = Web3(Web3.HTTPProvider(rpc_url4))
print(colored(Hecoinfo.isConnected(),"cyan"))

url_solona = 'https://api.testnet.solana.com'
# url_solona = 'https://api.devnet.solana.com'


##--------------------------- FUNCTION DEFINATIONS -------------------------------------------##

    
def get_balance(par):
    if flask.request.method == 'POST':
        try:
            if par and par['v_address']!= "" and par['v_address']!= None :
                address = par['v_address']
                solona_address = par['solona_address']
                algod_address = par['algod_address']
            else : 
                address = request.form['v_address']
                solona_address = request.form['solona_address']
                algod_address = request.form['algod_address']
                

        except:
            return {"data": {}, "status": False, "message": "Not all Paramaters Passed"}, 400

        try:
            ether_balance = Ether.eth.get_balance(address)
            ether = Ether.fromWei(ether_balance, 'ether')

            bnb_balance = BNB.eth.get_balance(address)
            bnb = BNB.fromWei(bnb_balance, 'ether')

            polygon_balance = polygon.eth.get_balance(address)
            Polygon = polygon.fromWei(polygon_balance, 'ether')

            Fantom_balance = Fantom.eth.get_balance(address)
            fantom = Fantom.fromWei(Fantom_balance, 'ether')
            
            Hecoinfo_balance = Hecoinfo.eth.get_balance(address)
            hecoinfo = Hecoinfo.fromWei(Hecoinfo_balance, 'ether')

# ------API-Token---------------------#
            url = f"https://api.covalenthq.com/v1/42/address/{address}/balances_v2/?quote-currency=USD&format=JSON&nft=false&no-nft-fetch=false&key=ckey_373f6fe9f142487689b67de0e72"
          
            my_url = requests.get(url)
            Token=[]
            data = my_url.json()
            if  len(data) > 0:
                item_array = data['data']['items']
                for x in item_array:
                    name = (x["contract_name"])
                    balance = (x["balance"])
                    token_data = {
                        "contract_name" : str(name),
                        "balance" : int(balance)
                    }
                    Token.append(token_data)
                    # return json.dumps(Token)

##------------Solona-Balance--------------------##
                Lamport = 1000000000
                headers = {
                    'Content-type':'application/json', 
                    'Accept':'application/json'
                }
                data = {"jsonrpc":"2.0", "id":1, "method":"getBalance", "params":[f"{solona_address}"]}
                # data = {"jsonrpc":"2.0", "id":1, "method":"getBalance", "params":["4ETf86tK7b4W72f27kNLJLgRWi9UfJjgH4koHGUXMFtn"]}
                my_data = requests.post(url_solona,json=data, headers=headers)
                solona = my_data.json()
                solona_balance = solona['result']['value'] / Lamport
                # print (colored(solona_balance,'green'))
                
##--------------Algod-Balance------------------------##
                Lamport = 1000000
                headers = {
                    'x-api-key': 'r1hPXdqrtl3SjSh1LICs45wIjm7JB8p1TyFXMHEg', 
                    'Accept':'application/json' 
                }
                # url = 'https://mainnet-algorand.api.purestake.io/idx2/v2/accounts/GW6T5RAUWG5H6A4LP7UWL2PYGAZJUL6RCBWSU24PO27COCT3MMS6YCU2Z4'
                url = f'https://mainnet-algorand.api.purestake.io/idx2/v2/accounts/{algod_address}'
                my_data = requests.get(url,headers=headers)
                algod = my_data.json()
                algod_balance = algod['account']['amount']/ Lamport
                # print (colored(algod_balance,'green'))
##-----------------------------------------------##

                if request.form and request.form["form-submit"]:
                    response_data = {"ETH" : float(ether),"BSC" : float(bnb),"MATIC" : float(Polygon),"FTM" : float(fantom),
                        "HT" :float(hecoinfo),"solona" : float(solona_balance),"Algorand" :float(algod_balance)}
                    return render_template("index.html",data = response_data,jsonfile = Token,len = len(Token))
                
                else:
                    return {"balance data": {"ETH" : float(ether),"BSC" : float(bnb),"MATIC" : float(Polygon),
                        "FTM" : float(fantom), "HT" :float(hecoinfo)},"Token" : Token,"Solona" :solona_balance,"Algorand" :algod_balance, "status": True, "message": "Success"}, 200
        except Exception as e:
            print(e)
            return {"balance data":{}, "status": False, "message": "Failed"}, 400



def balance_form(par):
    if flask.request.method == 'GET':
            return render_template("index.html")

##-------------------------------------------Token Api Function--------------------------------------------------------##
def data(par):
    address = par['address']
    # currency = par['quote-currency']

    url = f"https://api.covalenthq.com/v1/42/address/{address}/balances_v2/?quote-currency=USD&format=JSON&nft=false&no-nft-fetch=false&key=ckey_373f6fe9f142487689b67de0e72"
    myy = requests.get(url)
    item_array=[]
    resArr=[]
    data = myy.json()
    if  len(data) > 0:
        item_array = data['data']['items']
        for x in item_array:
            resArr.append(x)
    return json.dumps(resArr)



##------------------------------ROUTE----------------------------------------##

@app.route('/get_balance',methods=['GET', 'POST'])
@cross_origin()
def get_balance_():      
    par = flask.request.json
    print(colored(par, "cyan"))
    response_data = get_balance(par)
    return response_data

@app.route('/',methods=['GET', 'POST'])
@cross_origin()
def balance_form_():      
    par = flask.request.json
    response_data = balance_form(par)
    return response_data
##-------------------------------------------Token Api Route--------------------------------------------------------##
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
    app.run(host="0.0.0.0", port=8888,debug=True)

