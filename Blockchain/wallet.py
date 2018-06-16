from _wallet import *
from wallet_cmd import *



if __name__ == '__main__':

    wallet = Wallet()
    command_prompt = Wallet_CMD(wallet)
    command_prompt.start()
