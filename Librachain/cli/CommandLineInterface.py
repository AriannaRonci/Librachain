import logging

import web3
from eth_utils import is_address
from web3 import Web3


class CommandLineInterface:

    def __init__(self):
        self.menu_options = {
            1: 'Register',
            2: 'Log in',
            3: 'Exit',
        }

    def print_menu(self):
        for key in self.menu_options.keys():
            print(key, '--', self.menu_options[key])

        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
            return

        if option == 1:
            print('Handle option \'Option 1: Register\'')
            self.register_menu()
        elif option == 2:
            print('Handle option \'Option 2: Log in\'')
            self.login_menu()
        elif option == 3:
            print('Handle option \'Option 3: Exit\'')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')

    def register_menu(self):
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7546"))

        print('Enter your wallet information.')
        public_key = input('Public Key:')
        print(is_address(public_key))

        private_key = input('Private Key:')
        private_key2 = input('Confirm Private Key:')

        pk = w3.eth.account.from_key(private_key)

        if (is_address(public_key) & (public_key == pk.address) & (private_key2 == private_key)):
            print('Enter your personal account information.')
            print('(in this way every time you log in or want to perform a transaction it will not be necessary'
                  ' to provide your private key, but the username and password that you will specify below)')
            username = input('Username')
            password = input('Password')
            password = input('Check Passoword')
        else:
            print('Sorry, but the specified public key and private key do not match any account.')




    def login_menu(self):
        pass


cli = CommandLineInterface()
while (True):
    cli.print_menu()
