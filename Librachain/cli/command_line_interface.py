import os
import re

from eth_utils import is_address
from web3 import Web3
from controllers.controller import Controller
from controllers.shards_controller import ShardsController
from session.session import Session

import getpass


class CommandLineInterface:

    def __init__(self, session: Session):

        self.controller = Controller(session)
        self.shards_controller = ShardsController()
        self.session = session

        self.menu_options = {
            1: 'Register',
            2: 'Log in',
            3: 'Exit',
        }

        self.wrong_input_options = {
            1: 'Retry',
            2: 'Exit',
        }

        self.user_options = {
            1: 'Deploy Smart Contract',
            2: 'Invoke Smart Contact\'s Method',
            3: 'Logout'
        }

    def print_menu(self):
        for key in self.menu_options.keys():
            print(key, '--', self.menu_options[key])

        try:
            option = int(input('Enter your choice: '))
        except ValueError:
            print('Wrong input. Please enter a number ...\n')
            self.print_menu()

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
            self.print_menu()

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
            self.print_menu()

        if (is_address(public_key) and (public_key == pk.address) and (private_key == check_private_key)):

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
            self.print_menu()

    def login_menu(self):

        if not self.controller.check_number_attempts() and self.session.get_time_left_for_unlock() < 0:
            self.session.reset_attempts()

        if self.session.get_time_left_for_unlock() <= 0 and self.controller.check_number_attempts():
            username = input('Username: ')
            password = getpass.getpass('Password: ')
            res = self.controller.login(username, password)

            if res == 0:
                print('\nYou are login\n')
                self.print_user_options()
            elif res == -1:
                print('\nIncorrect username or password\n')
                self.print_retry_exit_menu('login')
            # elif res == 'Max Attempts':
            # print('You have reached the maximum number of attempts')
            # return
        else:
            print('\nYou have reached the maximum number of attempts')
            print(f'Time left until next attempt: {int(self.session.get_time_left_for_unlock())} seconds\n')
            return

    def print_retry_exit_menu(self, predecessor_method):
        for key in self.wrong_input_options.keys():
            print(key, '--', self.wrong_input_options[key])

        try:
            option = int(input('Enter your choice: '))
        except ValueError:
            print('Wrong input. Please enter a number ...\n')
            self.print_retry_exit_menu(predecessor_method)

        if option == 1:
            print('\nHandle option \'Option 1: Retry\'')
            if predecessor_method == 'login':
                self.login_menu()
            elif predecessor_method == 'deploy':
                self.read_smart_contract()
        elif option == 2:
            print('\nHandle option \'Option 2: Exit\'\n')
            if predecessor_method == 'login':
                self.print_menu()
            elif predecessor_method == 'deploy':
                self.print_user_options()
        else:
            print('Invalid option. Please enter a number between 1 and 2.\n')
            self.print_retry_exit_menu(predecessor_method)

    def print_user_options(self):
        for key in self.user_options.keys():
            print(key, '--', self.user_options[key])

        try:
            option = int(input('Enter your choice: '))
        except ValueError:
            print('Wrong input. Please enter a number ...\n')
            self.print_user_options()

        if option == 1:
            print('\nHandle option \'Option 1: Deploy Smart Contract\'')
            self.deploy_menu()
        elif option == 2:
            print('\nHandle option \'Option 2: Invoke Smart Contract\' Method\'')
            self.invoke_method_menu()
        elif option == 3:
            print('\nHandle option \'Option 3: Exit\'\n')
            self.session.set_user(None)
            self.print_menu()
        else:
            print('Invalid option. Please enter a number between 1 and 4.\n')

    def deploy_menu(self):
        print('Before proceeding with the deployment of Smart Contract it is necessary to enter the password ')
        password = getpass.getpass('Password: ')
        res = self.controller.check_password(self.session.get_user().get_username(), password)
        if res:
            file_path = self.read_smart_contract()

            while (True):
                try:
                    gas_limit = int(input('Gas limit: '))
                    break
                except ValueError:
                    print('Wrong input. Please enter a number ...\n')

            while (True):
                try:
                    gas_price = int(input('Gas price: '))
                    break
                except ValueError:
                    print('Wrong input. Please enter a number ...\n')

            self.shards_controller.deploy_smart_contract(file_path, self.session.get_user().get_public_key(), gas_limit, gas_price)

        else:
            print('\nIncorrect password.\n Sorry but you can\'t proceed with the deployment of Smart Contract.\n')
            self.print_user_options()

    def read_smart_contract(self):
        file_path = input('Enter the path of your file: ')
        if not os.path.exists(file_path):
            print(f'I did not find the file at, {str(file_path)}.\n')
            self.print_retry_exit_menu('deploy')
        else:
            print('We found your file: Smart Contract loaded correctly!\n')
            return file_path



