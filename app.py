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

##---------------------------------------- Balance-URL -----------------------------------------------##

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

# url_solona = 'https://api.testnet.solana.com'
# url_solona = 'https://api.devnet.solana.com'

url_solona = 'https://api.mainnet-beta.solana.com'


##-------------------------------- FUNCTION DEFINATIONS -------------------------------------------##

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

# ------API-Blockchain-Token--------------#
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
            ETHER_token =mainObj['Ethereum']
            BSC_token =mainObj['Binance']
            MATIC_token =mainObj['Polygon_MATIC']
            FTM_token =mainObj['Fantom_FTM']
            HT_token =mainObj['Hecoinfo_HT']
            # print(mainObj) # return mainObj

##---------Solona-Balance-------##
            Lamport = 1000000000
            headers = {
                'Content-type':'application/json', 
                'Accept':'application/json'
            }
            data = {"jsonrpc":"2.0", "id":1, "method":"getBalance", "params":[f"{solona_address}"]}
            my_data = requests.post(url_solona,json=data, headers=headers)
            solona = my_data.json()
            solona_balance = solona['result']['value'] / Lamport     
##------------Solona-Token-Balance--------------------##
            headers = {
            'Content-type':'application/json', 
            'Accept':'application/json' 
            }
            solana_url_token = f'https://public-api.solscan.io/account/tokens?account={solona_address}'

            solana_token = requests.get(solana_url_token,headers=headers)
            token = solana_token.json()
            SolanaToken = {}
            if  len(token) > 0:
                tokenArr = token
                for x in  tokenArr:
                    name = "None"
                    if (x['tokenName']):
                        name = (x['tokenName'])
                    balance = "None"
                    if (x['tokenAmount']['amount']):
                        balance = (x['tokenAmount']['amount'])
                    SolanaToken[str(name)]=int(balance)
                    # print(SolanaToken)

       
##------Algod-Balance-------##
            Lamport = 1000000
            headers = {
                'x-api-key': 'r1hPXdqrtl3SjSh1LICs45wIjm7JB8p1TyFXMHEg', 
                'Accept':'application/json' 
            }
            url = f'https://mainnet-algorand.api.purestake.io/idx2/v2/accounts/{algod_address}'
            my_data = requests.get(url,headers=headers)
            algod = my_data.json()
            algod_balance = algod['account']['amount'] / Lamport
##---------------------------##

            if request.form and request.form["form-submit"]:
                response_data = {"ETH" : float(ether),"BSC" : float(bnb),"MATIC" : float(Polygon),"FTM" : float(fantom),
                    "HT" :float(hecoinfo),"solona" : float(solona_balance),"Algorand" :float(algod_balance)}
                return render_template("index.html",data = response_data,jsonfile = mainObj,len = len(mainObj),TokenSolana = SolanaToken)
            
            
            else:
                ether_responce = {"balance" : float(ether),"Token" : ETHER_token}
                bsc_responce = {"balance" : float(bnb),"Token" : BSC_token}
                polygon_responce = {"balance" : float(Polygon),"Token" : MATIC_token}
                fantom_responce = {"balance" : float(fantom),"Token" : FTM_token}
                hecoinfo_responce = {"balance" : float(hecoinfo),"Token" : HT_token}
                solana_responce = {"balance" : float(solona_balance),"Token" : SolanaToken}
                algo_responce = {"balance" : float(algod_balance)}

                main_obj = {"Ethereum" : ether_responce,"Binance" : bsc_responce,
                    "Polygon" : polygon_responce,"Fantom" :fantom_responce,"Hecoinfo":hecoinfo_responce,"Solana":solana_responce,"Algorand" : algo_responce}
                return main_obj
        except Exception as e:
            print(e)
            return {"balance data":{}, "status": False, "message": "Failed"}, 400



def balance_form(par):
    if flask.request.method == 'GET':
            return render_template("index.html")

##-----Blockchain-Toke-Api-Function---##
def getTokenData(url):
    tokenData = requests.get(url)
    Token = {}
    jsontokenData = tokenData.json()
    Lamport = 1000000000000000000  
    if  len(jsontokenData) > 0:
        tokenArr = jsontokenData['data']['items']
        for x in  tokenArr:
            name = (x["contract_name"])
            balance = (x["balance"])
            Token[str(name)]=int(balance) /Lamport            
        return Token  

##-------------------------------------------ROUTE----------------------------------------------------##

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888,debug=True)

