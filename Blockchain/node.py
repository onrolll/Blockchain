from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, jsonify
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, IntegerField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

from time import time
from urllib.parse import urlparse
from uuid import uuid4

from pycoin.ecdsa import generator_secp256k1, sign,verify
import hashlib, bitcoin, json

import _transaction, _block, _node

from pprint import pprint
from _hashing import *


app = Flask(__name__)

node = _node.Node()
print("AND THOSE ARE node.pending_transactions AT SERVER CREATION", node.pending_transactions)
"""
genesis_tran ={
"from_address": "Genesis_Address",
"is_verified": 1,
"paid": 1,
"sender_public_key": 'Genesis_Public_Key',
"sender_signature": 'Genesis_Signature',
"timestamp": "666",
"to_address": "285970d8f0c438ccc5b379c0dc1f8502e91a6e6b",
"transaction_sha256hex": "Genesis_Hash",
"transaction_value": 1000000
}
node.pending_transactions.append(json.dumps(genesis_tran))
"""
@app.route('/')
def home():
    return "Node is running",200

@app.route('/new_transaction',methods = ['POST'])
def new_transaction():
    values = request.get_json()
    #print(values)
    required = ['from_address','to_address','transaction_value','timestamp',
                'sender_public_key','transaction_sha256hex','sender_signature']

    if not all(k in values for k in required):
        return 'Missing values',400
    transaction = _transaction.Transaction(from_address=values['from_address'],
                                           to_address=values['to_address'],
                                           transaction_value=values['transaction_value'],
                                           sender_public_key=values['sender_public_key'],
                                           timestamp=values['timestamp'],
                                           transaction_sha256hex=values['transaction_sha256hex'],
                                           sender_signature=values['sender_signature'],
                                           is_verified=verify_transaction(values['sender_public_key'],values['transaction_sha256hex'],values['sender_signature'])
                                           )
    if not verify_transaction(values['sender_public_key'],values['transaction_sha256hex'],values['sender_signature']):
        return 'Invalid Signature',400
    print("Pending Transactions before node.pending_transactions.append(json.dumps(transaction.__dict__)) --->>",node.pending_transactions)
    #Problem with the below solution: return type str; should be dict
    #node.pending_transactions.append(json.dumps(transaction.__dict__))

    #Handling the above Problem
    print("type(jsonify(transactions.__dict__))",type(jsonify(transaction.__dict__)))
    node.pending_transactions.append(transaction.__dict__)
    print('-----------+++++++++++++++')
    print("Pending Transactions after node.pending_transactions.append(transaction) -->>",node.pending_transactions)

    #TODO verify transaction hash!

    #This should go to the wallet; returns a dict
    return jsonify(transaction.__dict__),200

@app.route('/get_mining_job/<string:miner_address>',methods=['GET'])
def get_mining_job(miner_address):
    #if block:
        #block.clear()


    block_to_mine = len(node.blockchain)
    node.miners_block_map[miner_address] = block_to_mine
    print("node.pending_transactions:",node.pending_transactions)
    # block_transactions must match
    if not node.block_transactions:
        # Should be here at least once
        print("in if not node.block_transactions:")
        print("node.pending_transactions:",node.pending_transactions)
        node.block_transactions = node.pending_transactions
        print("node.block_transactions",node.block_transactions)

    print("out if not node.block_transactions:")
    print("node.block_transactions out of if",node.block_transactions)
    # Must have a previous_block_sha256hex
    prev_block_hash ="Genesis Block Hash"

    last_block = _node.last_block(node.blockchain)
    print('Last_block')
    print(last_block)
    print('Last_block')
    if  last_block:
        print('In :if  last_block:')
        print(last_block['block_hash'])
        prev_block_hash = last_block['block_hash']


    block = _block.Block(index=len(node.blockchain),miner_address=miner_address,
                         transactions=node.block_transactions,previous_block_sha256hex=prev_block_hash)
    print("Block's transactions as sent to the miner, but before node.pending_transactions = [] -->>", block.transactions)
    #put true and false in "" for this example to work
    """
    transaction = {
                "from_address": "285970d8f0c438ccc5b379c0dc1f8502e91a6e6a",
                "is_verified": "true",
                "paid": "false",
                "sender_public_key": [
                    [
                        8.5363362928665052468517452353061258797903474564059646721822368387960575747825e+76,
                        5.7993131043030597910995642810638880203206439805135226524116736542324177391178e+76
                    ]
                ],
                "sender_signature": [
                    [
                        3.3564970511139248083057722266866482150873649814278646135889838888796744204332e+76,
                        3.198097823345511491473779854126608436165659742371942157620398348871469737965e+76
                    ]
                ],
                "timestamp": "2018-03-08 14:12:51",
                "to_address": "285970d8f0c438ccc5b379c0dc1f8502e91a6e6b",
                "transaction_sha256hex": "f3b0a63d25345a04ec17676dd7f2131ab323701622fd9c16fd1692cc9d07f105",
                "transaction_value": 1.3234
                }
    block.transactions.append(transaction)
    """
    node.pending_transactions = []
    print("Block's transactions as sent to the miner", block.transactions)
    return jsonify(block.__dict__)


@app.route('/candidate_block',methods = ['POST'])
def candidate_block():
    block = request.get_json()
    print(block)

    # Makes sure the block is the one from node's miners_block_map
    if node.miners_block_map[block['miner_address']] != block['index']:
        response = {
        'msg':'Sorry, this block was not for mining'
        }
        return jsonify(response),400

    # Makes sure the block is not out of date
    if len(node.blockchain)!=block['index']:
        response = {
        'msg':'Sorry, this block is out of date. Someone was faster :('
        }
        return jsonify(response),400




    response = {
    'msg':'Block will be validated and then added to the chain'
    }

    block_hash = block['block_hash']

    block['block_hash']="Genesis Block Hash"

    # Checks if the block_hash matches the sha256hex of the block.
    # Note that we first replace the block['block_hash'] with "Genesis Block Hash"
    # as this represents the state of the block when the miner found the block
    if  block_hash != sha256hex(block):
        response = {
        'msg':'Invalid block hash!'
        }
        return jsonify(response),400

    # If we got here then hashes match
    print('Proof of Work is Valid!')

    # Revert block['block_hash'] value
    block['block_hash']= block_hash

    # Reset node's block_transactions
    for trans in node.block_transactions:
        print("This is a trans -> ",trans)
        print("This is type(trans) -> ",print(type(trans)))


        #TODO check if there is liquidity in address_balance
        """
        if not node.address_balance[trans['from_address']]:
            node.address_balance[trans['from_address']] = 0
        node.address_balance[trans['from_address']] -= trans['transaction_value']
        """
        node.address_balance[trans['from_address']] = node.address_balance.get(trans['from_address'],0) - int(trans['transaction_value'])

        """
        if not node.address_balance[trams['to_address']]:
            node.address_balance[trams['to_address']] = 0
        node.address_balance[trams['to_address']] += trans['transaction_value']
        """


        node.address_balance[trans['to_address']] = node.address_balance.get(trans['to_address'],0) + int(trans['transaction_value'])

    print("Node address_balance before node.block_transactions.clear()",node.address_balance)

    node.block_transactions.clear()

    print("Node address_balance after node.block_transactions.clear()",node.address_balance)

    node.blockchain.append(block)
    return jsonify(response),200

@app.route('/chain', methods=['GET'])
def chain():
    return jsonify(node.blockchain)

@app.route('/difficulty', methods=['GET'])
def difficulty():
    dif = _node.calculate_cumulative_difficulty(node.blockchain)
    return jsonify(dif)

@app.route('/balance/<string:address>', methods = ['GET'])
def balance(address):
    print("ADDRESSS IN balance -------------")
    print(address)
    #trimmed_address = address[2: len(address) - 2]
    print(address[2: len(address) - 2])
    balance = node.address_balance[address]
    print(balance)
    print("ADDRESSS IN balance -------------")



    return jsonify(balance)

def verify_transaction(pub_key,transaction_sha256hex,signature):
    #if len(self.sender_signature)>0:
    #pub_key = transaction.sender_public_key
    #signature = transaction.sender_signature

    return verify(generator_secp256k1, pub_key, int(transaction_sha256hex,16), signature)
    #return "no signature"

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port,debug=True)
