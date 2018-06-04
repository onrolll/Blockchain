import cmd,sys
from pprint import pprint

class Wallet_CMD(cmd.Cmd):
    def __init__(self, _wallet):
        super().__init__()
        self.wallet = _wallet
        self.prompt = '> '
        self.cmdloop('Starting prompt...')



    def do_generate(self, wallet):

        self.wallet.random_private_key_to_address()


    def do_take_my_key(self, wallet, args):

        self.wallet.existing_private_key_to_address(args)
        #


    def do_addresses(self,wallet):
        pprint(self.wallet.addresses)
"""
    def parse(arg):
        'Convert a series of zero or more numbers to an argument tuple'
        return tuple(map(str, arg.split()))
"""
