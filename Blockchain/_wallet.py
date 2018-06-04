from pycoin.ecdsa import generator_secp256k1, sign
import hashlib, bitcoin, json, _hashing


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

        address = self.ripemd160(public_key_compressed)
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

        address = ripemd160(public_key_compressed)
        print("blockchain address:", address)
        print("-----------------------------------------------")
        print("-----------------------------------------------")

    def ripemd160(self, public_key_compressed):
        hash_bytes = hashlib.new('ripemd160', public_key_compressed.encode("utf8")).digest()
        return hash_bytes.hex()
