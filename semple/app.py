#!/usr/bin/env python3
import ast
import flask
import requests
import firebase_admin
import time
from time import strftime, gmtime
from datetime import datetime
from flask_cors import CORS, cross_origin
from firebase_admin import credentials
from firebase_admin import firestore
from termcolor import colored
from db_mysql import (add_access_token, add_item, remove_item, 
                get_token_from_db)

#------------------------------------------------------------------------------#
#GLOBALS
# Use the application default credentials
cred = credentials.Certificate('pos-int-9566f0d8bd72.json')
firebase_admin.initialize_app(cred, {'projectId': 'pos-int'})

db = firestore.client()

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#------------------------------------------------------------------------------#
#Cloud Firebase Methods
def add_document(collection, document, data:dict):
    doc_ref = db.collection(collection). document(document)
    doc_ref.set(data)

# def update_document(collection, document, data:dict):
#     doc_ref = db.collection(collection).document(document)
#     doc_ref.update(data)
    
# def delete_document_field(collection, document, field_names:list):
#     doc_ref = db.collection(collection).document(document)
    
#     for field in field_names:
#         doc_ref.update({field: firestore.DELETE_FIELD})

# def get_documents(collection):
#     items = db.collection(collection)
#     docs = items.stream()

#     return docs

#------------------------------------------------------------------------------#

def token(par):
    try:
        mid = par['mid']
        token = par['token']
        token_type = par['token_type']
        
        timestamp = int(time.time())
    except:
        return {"data": {}, "status": False, "message": "Not all Paramaters Passed"}, 400
        
    try:
        response, status_code = add_access_token(mid, token, token_type, timestamp)
        return response, status_code
    except Exception as e:
        print(e)
        return {"data": {}, "status": False, "message": "Failed"}, 400
       
#------------------------------------------------------------------------------# 
        
def get_token(par):
    try:
        mid = par['mid']
        token_type = par['token_type']
    except:
        return {"data": {}, "status": False, "message": "Not all Paramaters Passed"}, 400
        
    try:
        token = get_token_from_db(mid, token_type)
        return {"data": {"token": token}, "status": True, "message": "Success"}, 200
    except:
        return {"data": {}, "status": False, "message": "Failed"}, 400

#------------------------------------------------------------------------------#    
def add_item_to_db(par):
    try:
        mid = par['mid']
        item_id = par['item_id']
        code = par['code']
        name = par['name']
        price = par['price']
        quantity = par['quantity']
        token_type = par['token_type']
        timestamp = int(time.time())
    except:
        return {"data": {}, "status": False, "message": "Not all Paramaters Passed"}, 400
        
    try:
        response, status_code = add_item(mid, item_id, name, price, quantity, code, token_type, timestamp)
        return response, status_code
    except:
        return {"data": {}, "status": False, "message": "Failed"}, 400

#------------------------------------------------------------------------------#
  
# def sync(par):
#     try:
#         mid = par['mid']
#     except:
#         return {"data": {}, "status": False, "message": "Not all Paramaters Passed"}, 400
        
#     docs = get_documents(mid)

#     for doc in docs:
# #        print(f'{doc.id} => {doc.to_dict()}')    
#         par = {"mid": str(mid), 
#                "item_id": str(doc.to_dict()['id']), 
#                "name": str(doc.to_dict()['name']), 
#                "price": float(doc.to_dict()['price']), 
#                "quantity": float(doc.to_dict()['stockCount'])
#                }   
#         response, status_code = add_item_to_db(par)
        
#     return {"data": {}, "status": True, "message": "Synced"}, 201
    
    
#------------------------------------------------------------------------------#

def remove_item_from_db(par):
    try:
        mid = par['mid']
        item_id = par['item_id']
        token_type = par['token_type']
    except:
        return {"data": {}, "status": False, "message": "Not all Paramaters Passed"}, 400
        
    try:
        if token_type == 'C':
            db.collection(mid).document(item_id).delete()
        response, status_code = remove_item(mid, item_id, token_type)
        return response, status_code
    except:
        return {"data": {}, "status": False, "message": "Failed"}, 400
        
#------------------------------------------------------------------------------#

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)
    
#------------------------------------------------------------------------------#

def process_callback(par):
    try:
        for merchant, items in par['merchants'].items():
            for item in items:
                operation = item['objectId'].split(":")[0].upper()
                item_id = item['objectId'].split(":")[-1]
                item_type = item['type']
                ts = item['ts']
                token_type = 'C'
                timestamp = int(time.time())
                
                print(colored((ts, item_id, item_type), "green"))
                
                clover_access_token = get_token_from_db(merchant, token_type)
                clover_item_dict = requests.get(f"https://apisandbox.dev.clover.com/v3/merchants/{merchant}/items/{item_id}?access_token={clover_access_token}").json()
                
                if 'id' in clover_item_dict.keys():
                    clover_item_stock_dict = requests.get(f"https://apisandbox.dev.clover.com/v3/merchants/{merchant}/item_stocks/{item_id}?access_token={clover_access_token}").json()     
                    name = clover_item_dict['name']
                    price = clover_item_dict['price']
                    try:
                        stock = clover_item_stock_dict['stockCount']
                    except:
                        stock = 0
                        
                    try:
                        code = clover_item_dict['code']
                    except:
                        code = ""                    
                        
                    if item_type == "UPDATE" and operation=='I':
                        add_document(merchant, item_id, {'id': item_id, 'name': name, 'price': price, 'stockCount': stock, 'code': code})
                        add_item(merchant, item_id, name, price, stock, code, token_type, timestamp)
                    elif item_type == "CREATE" and operation=='I':
                        add_document(merchant, item_id, {'id': item_id, 'name': name, 'price': price, 'stockCount': stock, 'code': code})
                        add_item(merchant, item_id, name, price, stock, code, token_type, timestamp)
                    else:
                        print(colored("type is invalid","red"))
                elif item_type == "DELETE" and operation=='I':
                    db.collection(merchant).document(item_id).delete()
                    remove_item(merchant, item_id, token_type)
                else:
                    print("OTHER CASE")

        return {"data": {}, "status": True, "message": "Success"}, 200

    except Exception as e:
        print(e)
        return {"data": {}, "status": False, "message": "Failed"}, 400

#------------------------------------------------------------------------------#

def squarecallback_post(par):
    timestamp = int(time.time())
    token_type = 'S'

    try:
        stock = par['data']['object']['inventory_counts'][0]['quantity']
        mid = par['merchant_id']
        catalog_object_id = par['data']['object']['inventory_counts'][0]['catalog_object_id']
    except Exception as e:
        print(e)
        return {"data": {}, "status": False, "message": "Invalid Parameters From Callback"}, 200

    try:
        squareup_access_token = get_token_from_db(mid, token_type)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {squareup_access_token}"}
        catalog_dict = requests.get(f"https://connect.squareupsandbox.com/v2/catalog/object/{catalog_object_id}", headers=headers).json()
        item_id = catalog_dict['object']['item_variation_data']['item_id']
        item_dict = requests.get(f"https://connect.squareupsandbox.com/v2/catalog/object/{item_id}", headers=headers).json()
        try:
            name = item_dict["object"]["item_data"]["name"]
        except:
            name = ""

        try:
            price = item_dict["object"]["item_data"]["variations"][0]["item_variation_data"]["price_money"]["amount"]
        except:
            price = 0

        try:
            code = item_dict["object"]["item_data"]["variations"][0]["item_variation_data"]['upc']
        except:
            code = ""

        add_item(mid, item_id, name, price, stock, code, token_type, timestamp)
        add_document(mid, item_id, {'id': item_id, 'name': name, 'price': price, 'stockCount': stock, 'code': code})

        return {"data": {}, "status": True, "message"   : "Success"}, 200
    except:
        return {"data": {}, "status": False, "message": "Success"}, 200

#------------------------------------------------------------------------------#

@app.route('/', methods=['GET'])
@cross_origin()
def pos_system():      
	
	return "Ojaexpress POS System", 200

@app.route('/token', methods=['POST'])
@cross_origin()
def token_():      
    par = flask.request.json
    print(colored(par, "cyan"))
    response, status_code = token(par)
	
    return response, status_code
    
@app.route('/get_token', methods=['POST'])
@cross_origin()
def get_token_():      
    par = flask.request.json
    print(colored(par, "cyan"))
    response, status_code = get_token(par)
	
    return response, status_code
    
@app.route('/add_item_to_db', methods=['POST'])
@cross_origin()
def add_item_to_db_():      
    par = flask.request.json
    print(colored(par, "cyan"))
    response, status_code = add_item_to_db(par)
	
    return response, status_code
    
@app.route('/remove_item_from_db', methods=['POST'])
@cross_origin()
def remove_item_from_db_():      
    par = flask.request.json
    response, status_code = remove_item_from_db(par)
	
    return response, status_code

@app.route('/pos_callback', methods=['POST'])
@cross_origin()
def process_callback_():      
    par = flask.request.json
    print(colored(par, "cyan"))
    if 'verificationCode' in par.keys():
        return "", 200
    response, status_code = process_callback(par)
	
    return response, status_code
    
@app.route('/squarecallback', methods=['GET'])
@cross_origin()
def squarecallback_get():           
    with open('squarecallback.txt', 'r') as f:
        content = f.read()
        
    return flask.render_template("squareupcallback.html", content=content)
    
@app.route('/squarecallback', methods=['POST'])
@cross_origin()
def squarecallback_post_():      
    par = flask.request.data
    dict_str = par.decode("UTF-8")
    par = ast.literal_eval(dict_str)
    print(colored(par, "cyan"))
    line_prepender('squarecallback.txt', str(par))
    response, status_code = squarecallback_post(par)
	
    return response, status_code
    
# @app.route('/sync', methods=['POST'])
# @cross_origin()
# def sync_():      
#     par = flask.request.json
#     print(colored(par, "cyan"))
#     response, status_code = sync(par)
	
#     return response, status_code
    
@app.route('/logs', methods=['GET'])
@cross_origin()
def logs_():      
    with open('screenlog.0', 'r') as f:
        content = f.read()
        
    return flask.render_template("log.html", content=content)
	
@app.route('/cloverproductioncallback', methods=['GET','POST'])
@cross_origin()
def cloverproductioncallback():      
    if flask.request.method == 'GET':
        return "cloverproductioncallback"
	    
    elif flask.request.method == 'POST':
        print(flask.request.data)
        response_data = {"data": {}, "status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    else:
        response_data = {"data": {}, "status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400

@app.route('/squareproductioncallback', methods=['GET','POST'])
@cross_origin()
def squareproductioncallback():      
    if flask.request.method == 'GET':
        return "squareproductioncallback"
	    
    elif flask.request.method == 'POST':
        print(flask.request.data)
        response_data = {"data": {}, "status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    else:
        response_data = {"data": {}, "status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400
        
@app.route('/vendposcallback', methods=['GET','POST'])
@cross_origin()
def vendposcallback():      
    if flask.request.method == 'GET':
        return "vendposcallback"
	    
    elif flask.request.method == 'POST':
        print(flask.request.data)
        response_data = {"data": {}, "status": True, "message": "Success"}
        return flask.jsonify(response_data), 200

    else:
        response_data = {"data": {}, "status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400
        
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=80,debug=True)



