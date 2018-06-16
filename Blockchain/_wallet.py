from pycoin.ecdsa import generator_secp256k1, sign
import hashlib, bitcoin, json, _hashing, _transaction, requests as r


class Wallet(object):

    def __init__(self):
        self.addresses = {}
        self.node_url = "http://127.0.0.1:5000/"




    def random_private_key_to_address(self):
        print("Random private key --> public key --> address")
        print("---------------------------------------------")

        private_key_hex = bitcoin.random_key()
        print("private key (hex):", private_key_hex)
        print("---------------------------------------------")

        private_key = int(private_key_hex, 16)
        print("private key:", private_key)
        print("---------------------------------------------")

        public_key = (generator_secp256k1 * private_key).pair()
        print("public key:", public_key)
        print("---------------------------------------------")

        public_key_compressed = hex(public_key[0])[2:] + str(public_key[1] % 2)
        print("public key (compressed):", public_key_compressed)
        print("---------------------------------------------")

        address = _hashing.ripemd160(public_key_compressed)
        print("blockchain address:", address)
        print("---------------------------------------------")
        print("---------------------------------------------")

        self.addresses[address] = {
                                    'private_key_hex':private_key_hex,
                                    'private_key_int':private_key,
                                    'public_key_tuple':public_key,
                                    'public_key_compressed':public_key_compressed
                                    }



    def existing_private_key_to_address(self, private_key_hex):
        print("Existing private key --> public key --> address")
        print("-----------------------------------------------")

        print("private key (hex):", private_key_hex)
        print("-----------------------------------------------")

        private_key = int(private_key_hex, 16)
        print("private key:", private_key)
        print("-----------------------------------------------")

        public_key = (generator_secp256k1 * private_key).pair()
        print("public key:", public_key)
        print("-----------------------------------------------")

        public_key_compressed = hex(public_key[0])[2:] + str(public_key[1] % 2)
        print("public key (compressed):", public_key_compressed)
        print("-----------------------------------------------")

        address = _hashing.ripemd160(public_key_compressed)
        print("blockchain address:", address)
        print("-----------------------------------------------")
        print("-----------------------------------------------")

        self.addresses[address] = {
                                    'private_key_hex':private_key_hex,
                                    'private_key_int':private_key,
                                    'public_key_tuple':public_key,
                                    'public_key_compressed':public_key_compressed
                                    }



    def send(self, fromA, val, to):
        print(fromA)
        address_info = self.addresses[fromA]
        sender_public_key = address_info['public_key_tuple']


        transaction = _transaction.Transaction(from_address=fromA,to_address = to,transaction_value=val,sender_public_key=sender_public_key)
        pk=address_info['private_key_int']
        transaction.sender_signature = sign_transaction(transaction, pk)
        #sending a request to the node
        headers = {'content-type': 'application/json'}
        data = json.dumps(transaction.__dict__)
        post = r.post('%snew_transaction'%(self.node_url), data=data, headers=headers)
        print(post.json())

def sign_transaction(transaction, sender_priv_key:int):
    #transaction.sender_signature.append(sign(generator_secp256k1, sender_priv_key, int(self.transaction_sha256hex,16)))
    return sign(generator_secp256k1, sender_priv_key, int(transaction.transaction_sha256hex,16))
