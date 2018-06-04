
from flask.json import JSONEncoder
from _transaction import *
from _block import *


class DesJSONEncoder(JSONEncoder):
    def default(self, obj):
        """
        Serialize object to JSON
        :param obj: <object>
        :return: <json object>
        """
        if isinstance(obj, Block):
            return {
                'index': obj.index,
                'previous_block_sha256hex': obj.previous_block_sha256hex,
                'transactions': obj.transactions,
                'miner_address': obj.miner_address,
                'difficulty': obj.difficulty,
                'nonce': obj.nonce,
                'block_hash': obj.block_hash,
                'timestamp': obj.timestamp
                #obj.timestamp()?
            }
        if isinstance(obj, Transaction):

            return {
                'from_address': obj.from_address,
                'to_address': obj.to_address,
                'transaction_value': obj.transaction_value,
                'sender_public_key': str(obj.sender_public_key),
                'timestamp': obj.timestamp,
                'transaction_sha256hex': obj.transaction_sha256hex,
                'sender_signature': str(obj.sender_signature),
                'is_verified': str(obj.is_verified),
                'paid': str(obj.paid)

            }
        return super(DesJSONEncoder, self).default(obj)


def json_block_decoder(obj):
    """
    Deserialize json object to Block object
    :param obj: <json object>
    :return: <Block>


    """
    if 'block_hash' in obj and 'miner_address' in obj:
        transactions = []
        for transaction in obj['transactions']:
            transactions.append(json_transaction_decoder(transaction))
        # TODO check if cast needs to be done just in case
        return Block(index=obj['index'],
                     previous_block_sha256hex=obj['previous_block_sha256hex'],
                     transactions=transactions,
                     miner_address=obj['miner_address'],
                     difficulty=obj['difficulty'],
                     nonce=obj['nonce'],
                     block_hash=obj['block_hash'],
                     timestamp=obj['timestamp'])
    return obj


def json_transaction_decoder(obj):
    """
    Deserialize json object to Transaction object
    :param obj: <json object>
    :return: <Transaction>

    """
    if 'to_address' in obj and 'transaction_value' in obj:
        return Transaction(from_address=obj['from_address'],
                           to_address=obj['to_address'],
                           transaction_value=float(obj['transaction_value']),
                           sender_public_key=tuple(float(x) for x in obj['sender_public_key']),
                           timestamp=obj['timestamp'],
                           transaction_sha256hex=obj['transaction_sha256hex'],
                           sender_signature = tuple(float(x) for x in obj['sender_signature']),
                           is_verified=obj['is_verified'],
                           paid=obj['paid'])

    return obj
