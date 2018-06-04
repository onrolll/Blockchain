#from apscheduler.schedulers.background import BackgroundScheduler
import time, requests as r, json
from _hashing import sha256hex, timestamp
class Miner(object):
    def __init__(self):
        self.address = "285970d8f0c438ccc5b379c0dc1f8502e91a6e6a"
        self.node_url = "http://127.0.0.1:5000/"
        print("proceeding to start")
        self.start()

    def start(self):

        while 1:
            print("about to get mining job")
            block = self.get_mining_job()
            print("should have a mining job")
            if block:
                print("we in the IFFF")
                candidate_block = self.proof_of_work(block)
                self.post_mining_job(candidate_block)

            time.sleep(20)


    def get_mining_job(self):
        req = r.get('%sget_mining_job/%s'%(self.node_url,self.address))
        block = req.json()
        print(block)
        return block

    def proof_of_work(self, block):
        while 1:
            if block['nonce']%51331 == 0:
                print(block['nonce'])
                block['timestamp'] = timestamp()
            candidate_block_sha256hex = sha256hex(block)
            if candidate_block_sha256hex[:block['difficulty']]=="0"*block['difficulty']:
                print(candidate_block_sha256hex)
                block['block_hash'] = candidate_block_sha256hex
                return block
            block['nonce']+=1

    def post_mining_job(self, candidate_block):
        headers = {'content-type': 'application/json'}
        data = json.dumps(candidate_block)

        post = r.post('%scandidate_block'%(self.node_url), data=data, headers=headers)
        print(post.json())
        #time.sleep(100)
Miner()
