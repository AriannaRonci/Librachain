import re

from eth_utils import is_address
from web3 import Web3
from controllers.controller import Controller

import getpass


class CommandLineInterface:

    def __init__(self, session):

        self.controller = Controller(session)
        self.session = session

        self.menu_options = {
            1: 'Register',
            2: 'Log in',
            3: 'Exit',
        }

        self.wrong_login_options = {
            1: 'Retry',
            2: 'Exit',
        }

    def print_menu(self):
        for key in self.menu_options.keys():
            print(key, '--', self.menu_options[key])

        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...\n')
            return

        if option == 1:
            print('\nHandle option \'Option 1: Register\'')
            self.register_menu()
        elif option == 2:
            print('\nHandle option \'Option 2: Log in\'')
            self.login_menu()
        elif option == 3:
            print('\nHandle option \'Option 3: Exit\'')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.\n')

    def register_menu(self):
        w3 = Web3(Web3.HTTPProvider("http://0.0.0.0:8548"))

        print('Enter your wallet information.')
        public_key = input('Public Key: ')

        private_key = input('Private Key: ')
        # private_key = getpass.getpass('Private Key: ')
        check_private_key = input('Confirm Private Key: ', )
        # check_private_key = getpass.getpass('Confirm Private Key: ', )

        try:
            pk = w3.eth.account.from_key(private_key)
        except:
            print('Sorry, but the specified public key and private key do not match any account.\n')
            return

        if (is_address(public_key) and (public_key == pk.address)  (private_key == check_private_key)):

            print('Enter your personal account information.')
            print('(in this way every time you log in or want to perform a transaction it will not be necessary\n'
                  ' to provide your private key, but the username and password that you will specify below)')
            username = input('Username: ')

            while (True):
                # password = getpass.getpass('Password: ')
                # check_password = getpass.getpass('Confirm Passoword: ')
                password = input('Password: ')

                check_password = input('Confirm Passoword: ')
                if not re.fullmatch(r'(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z0-9@#$%^&+=]{10,255}', password):
                    print(
                        'Passoword must contains at least 10 symbols, at least one digit, at least one uppercase letter, at least one lowercase letter\n')
                elif (password != check_password):
                    print('Password and confirm password do not match')
                else:
                    break

            res = self.controller.register(username, password, public_key, private_key)
            if res:
                print('Registration was successful!\n')
            else:
                print('Sorry, but something went wrong!\n')

        else:
            print('Sorry, but the specified public key and private key do not match any account.\n')
            return

    def login_menu(self):

        if not self.controller.check_number_attempts() and self.session.getTimeLeftForUnlock() < 0:
            self.session.resetAttempts()

        if self.session.getTimeLeftForUnlock() <= 0 and self.controller.check_number_attempts():
            username = input('Username: ')
            password = getpass.getpass('Password: ')
            res = self.controller.login(username, password)

            if res == 0:
                print('\nYou are login\n')
                return
            elif res == -1:
                print('\nIncorrect username or password\n')
                self.retry_exit_menu()
            #elif res == 'Max Attempts':
                #print('You have reached the maximum number of attempts')
                #return
        else:
            print('\nYou have reached the maximum number of attempts')
            print(f'Time left until next attempt: {int(self.session.getTimeLeftForUnlock())} seconds\n')
            return


    def retry_exit_menu(self):
        for key in self.wrong_login_options.keys():
            print(key, '--', self.wrong_login_options[key])

        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...\n')
            self.retry_exit_menu()

        if option == 1:
            print('\nHandle option \'Option 1: Login\'')
            self.login_menu()
        elif option == 2:
            self.print_menu()
        else:
            print('Invalid option. Please enter a number between 1 and 2.\n')
            self.retry_exit_menu()


