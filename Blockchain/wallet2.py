import cmd,sys
from pprint import pprint

from pycoin.ecdsa import generator_secp256k1, sign
import hashlib, bitcoin, json, _hashing,requests as r
from _transaction import Transaction




class Wallet_CMD(cmd.Cmd):
    """
    def __init__(self):
        super().__init__()

        self.prompt = '> '
        self.cmdloop('Starting prompt...')

        self.addresses = {}
        self.node_url = "http://127.0.0.1:5000/"
"""

    intro = 'Welcome to the wallet shell. \n'
    prompt = '(wallet) '
    addresses  = {}
    node_url = "http://127.0.0.1:5000/"

    def do_generate(self,whatisthisArg):

        a,b = random_private_key_to_address()
        self.addresses[a]=b
        #print('+++++++++++++++++++++++++ \n'+ whatisthisArg + '++++++++++')

    def do_take_my_key(self, args):


        a,b = existing_private_key_to_address(args)
        self.addresses[a]=b


    def do_addresses(self,wallet):
        pprint(self.addresses)

    def do_send(self, args):
        tokens = args.split('/')
        receiver_address = tokens[0]
        value = int(tokens[1])
        from_address = tokens[2]
        address_info = self.addresses[from_address]
        sender_public_key = address_info['public_key_tuple']


        transaction = Transaction(from_address=from_address,to_address=receiver_address,transaction_value=value,sender_public_key=sender_public_key)
        pk=address_info['private_key_int']
        transaction.sender_signature = sign_transaction(transaction, pk)
        #sending a request to the node
        headers = {'content-type': 'application/json'}
        data = json.dumps(transaction.__dict__)
        post = r.post('%snew_transaction'%(self.node_url), data=data, headers=headers)
        print(post.json())



        """
            headers = {'content-type': 'application/json'}
            data = json.dumps(candidate_block)

            post = r.post('%scandidate_block'%(self.node_url), data=data, headers=headers)
        """


def sign_transaction(transaction, sender_priv_key:int):
    #transaction.sender_signature.append(sign(generator_secp256k1, sender_priv_key, int(self.transaction_sha256hex,16)))
    return sign(generator_secp256k1, sender_priv_key, int(transaction.transaction_sha256hex,16))

def random_private_key_to_address():
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

        address = ripemd160(public_key_compressed)
        print("blockchain address:", address)
        print("---------------------------------------------")
        print("---------------------------------------------")

        return address,{
                                    'private_key_hex':private_key_hex,
                                    'private_key_int':private_key,
                                    'public_key_tuple':public_key,
                                    'public_key_compressed':public_key_compressed
                                    }



def existing_private_key_to_address(private_key_hex):
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

        address = ripemd160(public_key_compressed)
        print("blockchain address:", address)
        print("-----------------------------------------------")
        print("-----------------------------------------------")
        return address,{
                                    'private_key_hex':private_key_hex,
                                    'private_key_int':private_key,
                                    'public_key_tuple':public_key,
                                    'public_key_compressed':public_key_compressed
                                    }

def ripemd160(public_key_compressed):
        hash_bytes = hashlib.new('ripemd160', public_key_compressed.encode("utf8")).digest()
        return hash_bytes.hex()

if __name__ == '__main__':


    Wallet_CMD().cmdloop()
