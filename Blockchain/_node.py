

class Node(object):
    def __init__(self):

        self.url = "http://127.0.0.1:5000"
        self.peers = set()
        self.pending_transactions = []
        genesis_tran ={
        "from_address": "Genesis_Address",
        "is_verified": True,
        "paid": True,
        "sender_public_key": 'Genesis_Public_Key',
        "sender_signature": 'Genesis_Signature',
        "timestamp": "666",
        "to_address": "285970d8f0c438ccc5b379c0dc1f8502e91a6e6b",
        "transaction_sha256hex": "Genesis_Hash",
        "transaction_value": 1000000
        }
        self.pending_transactions.append(genesis_tran)
        self.block_transactions = []
        self.blockchain = []
        self.cumulative_difficulty = calculate_cumulative_difficulty(self.blockchain)
        self.miners_block_map = {}
        self.last_block = last_block(self.blockchain)
        self.address_balance  = {}
        print('THOSE are PENDING TRANSACTIONS AT NODE CREATION',self.pending_transactions)

def calculate_cumulative_difficulty(blockchain):
            """
            Goes through the blockchain and sums the difficulty given the formula
            """
            difficulty = 0
            if len(blockchain)==0:
                return difficulty
            for block in blockchain:
                difficulty+= (block['difficulty'] * 256)
            return difficulty

def last_block(blockchain):

    """
    """

    if len(blockchain)>0:
        print('blockchain[-1]:',blockchain[-1])
        return blockchain[-1]
    return {}
