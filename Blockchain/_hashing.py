from passlib.hash import sha256_crypt
import hashlib, bitcoin, json,time,datetime



def sha256hex(block):
    """
    Creates a SHA-256 hash of a Block
    :param block: Block
    """

    # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
    block_bytes = json.dumps(block, sort_keys=True).encode('utf-8')
    return hashlib.sha256(block_bytes).hexdigest()



def timestamp():
    value = datetime.datetime.fromtimestamp(time.time())
    time_string = value.strftime('%Y-%m-%d %H:%M:%S')
    return time_string

def nakov_sha256(msg: str) -> int:
    hash_bytes = hashlib.sha256(msg.encode("utf8")).digest()
    return int.from_bytes(hash_bytes, byteorder="big")
