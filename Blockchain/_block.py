import _transaction, datetime, time

class Block(object):
    def __init__(self,
                 index=0,
                 previous_block_sha256hex = "",
                 transactions=[],
                 miner_address="Genesis Miner",
                 difficulty=4,
                 nonce=0,
                 block_hash="Genesis Block Hash",
                 timestamp=None):
        self.index = index
        self.previous_block_sha256hex = previous_block_sha256hex
        self.transactions = transactions
        self.miner_address = miner_address
        self.difficulty = difficulty
        self.nonce = nonce
        self.block_hash = block_hash
        self.timestamp = self.timestamp()
        #self.block_data_sha256hex =

    def timestamp(self):
        value = datetime.datetime.fromtimestamp(time.time())
        time_string = value.strftime('%Y-%m-%d %H:%M:%S')
        return time_string
