#!/usr/bin/env python3
import os
import json
import flask
import requests
import urllib.request
from PIL import Image
from termcolor import colored
from flask_cors import CORS, cross_origin

cwd = "."

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

PINATA_API_KEY = "23b39fcb3459d2cfb234"
PINATA_SECRET_API_KEY = "49581668d08420b22c0e648c7ba8df78c6e6c47dc6d1b085576cd36a5b1ad658"

def upload(filepath):

    file = [('file', open(filepath, 'rb'))]
    
    r = requests.post(
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS",
        headers = {
            "pinata_api_key": PINATA_API_KEY,
            "pinata_secret_api_key": PINATA_SECRET_API_KEY
        },
        files = file
    )

    return r.json()

def uploadToIPFS(par):
    # try:
    imageURL = par["imageURL"]
    tokenId = par["token_id"]
    filepath = os.path.join(cwd, f"files/{tokenId}")
    response = requests.get(imageURL)
    if response.status_code==200:
        print("Downloading "+ imageURL)
        with open(filepath, "wb") as f:
            f.write(response.content)
    else:
        try:
            urllib.request.urlretrieve(imageURL, filepath)
        except:
            print('URL not reachable')
            response_data = {"data": {}, "status": False, "message": "URL not reachable"}
            return response_data, 400
    
    imageResponse = upload(filepath)
    par["imageHash"] = imageResponse["IpfsHash"]
    os.remove(filepath)

    json_object = json.dumps(par, indent = 4)

    with open(filepath, "w") as f:
        f.write(json_object)

    jsonResponse = upload(filepath)

    os.remove(filepath)

    response_data = {"data": {"imageHash": imageResponse["IpfsHash"], "jsonHash": jsonResponse["IpfsHash"]}, "status": True, "message": "Success"}
    
    return response_data, 200
    # except:
    #     response_data = {"data": {}, "status": False, "message": "Failed"}
    #     return response_data, 400
	
@app.route('/uploadToIPFS', methods=['GET','POST'])
@cross_origin()
def uploadToIPFS_():      
    if flask.request.method == 'GET':
        return "Hey There"
    elif flask.request.method == 'POST':
        par = flask.request.json
        print(colored(par, "cyan"))
        response, status_code = uploadToIPFS(par)
        return response, status_code
    else:
        response_data = {"data": {}, "status": False, "message": "Wrong Method"}
        return flask.jsonify(response_data), 400
	
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000,debug=True)