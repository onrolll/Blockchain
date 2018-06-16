import cmd,sys
from pprint import pprint
import _hashing, sys
class Wallet_CMD(cmd.Cmd):
    def __init__(self, _wallet):
        super().__init__()
        self.wallet = _wallet
        self.prompt = '> '
        self.cmdloop('Starting prompt...')


    def do_send(self, args):

        from_address, amount, to_address = args.split(' ')
        self.wallet.send(from_address, amount, to_address)

    def do_generate(self, wallet):

        self.wallet.random_private_key_to_address()


    def do_take_my_key(self, args):

        self.wallet.existing_private_key_to_address(args)
        #


    def do_addresses(self,wallet):
        pprint(self.wallet.addresses)
