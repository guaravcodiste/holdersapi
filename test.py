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


def fetchData(dbPath, blockNumber):
    con = sqlite3.connect(dbPath)
    cur = con.cursor()

    fetchQuery = f'''SELECT * FROM firstevent WHERE BlockNumber <= {blockNumber} ORDER BY BlockNumber ASC'''
    cur.execute(fetchQuery)
    rows = cur.fetchall()

    con.commit()
    con.close()
    return rows

def main(blockNumber):
    rows = fetchData("./test.db", blockNumber)
    # print(rows)
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

    print(holdings)


if __name__ == "__main__":
    main(105)