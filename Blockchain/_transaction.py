import hashlib, bitcoin, json, time, datetime
from pycoin.ecdsa import generator_secp256k1, sign, verify
from passlib.hash import sha256_crypt
from _hashing import sha256hex





class Transaction(object):
    def __init__(self,from_address=None,
                to_address=None,
                transaction_value=None,
                sender_public_key=None,
                timestamp=None,
                transaction_sha256hex=None,
                sender_signature=None,
                is_verified=False,
                paid=False

                ):
        self.from_address = from_address
        self.to_address = to_address
        self.transaction_value =  transaction_value
        self.sender_public_key = sender_public_key
        self.timestamp  = self.transaction_timestamp()
        self.transaction_sha256hex = self.transaction_hash()
        self.sender_signature = sender_signature
        self.is_verified = is_verified
        self.paid = paid

    def transaction_hash(self):
        transaction = str(self.from_address) + str(self.to_address) + str(self.transaction_value) + str(self.timestamp) + str(self.sender_public_key)
        return sha256hex(transaction)

    #TODO: transfer functionality to wallet
    def sign_transaction(self, sender_priv_key:int):
        self.sender_signature.append(sign(generator_secp256k1, sender_priv_key, int(self.transaction_sha256hex,16)))
    def transaction_timestamp(self):
        value = datetime.datetime.fromtimestamp(time.time())
        time_string = value.strftime('%Y-%m-%d %H:%M:%S')
        return time_string

    #TODO: transfer functionality to node
    def verify_transaction(self):
        #if len(self.sender_signature)>0:
        pub_key = self.sender_public_key
        signature = self.sender_signature

        self.is_verified = verify(generator_secp256k1, pub_key, int(self.transaction_sha256hex,16), signature)
        #return "no signature"
