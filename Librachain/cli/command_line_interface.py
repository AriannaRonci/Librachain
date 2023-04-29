import os
import re

from colorama import Fore, Style
from eth_utils import is_address, decode_hex, ValidationError
from web3.exceptions import ContractLogicError, InvalidAddress

from controllers.controller import Controller
from controllers.shards_controller import ShardsController
from session.session import Session
from eth_keys import keys

import getpass


class CommandLineInterface:

    def __init__(self, session: Session):

        self.controller = Controller(session)
        self.shards_controller = ShardsController()
        self.session = session

        self.menu_options = {
            1: 'Register.',
            2: 'Log in.',
            3: 'Exit.',
        }

        self.wrong_input_options = {
            1: 'Retry.',
            2: 'Exit.',
        }

        self.user_options = {
            1: 'Deploy Smart Contract.',
            2: 'Invoke Smart Contract\'s Method.',
            3: 'Consult your Smart Contract in your local databese.',
            4: 'Delete Smart Contrat from your local database.',
            5: 'Logout.'
        }

    def print_menu(self):
        for key in self.menu_options.keys():
            print(key, '--', self.menu_options[key])

        try:
            option = int(input('Enter your choice: '))

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

        except ValueError:
            print('Wrong input. Please enter a number ...\n')
            self.print_menu()

    def register_menu(self):
        print('Enter your wallet information.')
        public_key = input('Public Key: ')
        private_key = input('Private Key: ')
        # private_key = getpass.getpass('Private Key: ')
        check_private_key = input('Confirm Private Key: ')
        # check_private_key = getpass.getpass('Confirm Private Key: ')

        try:
            priv_key_bytes = decode_hex(private_key)
            priv_key = keys.PrivateKey(priv_key_bytes)
            pk = priv_key.public_key.to_checksum_address()
        except Exception:
            print('Sorry, but the specified public key and private key do not match any account.\n')
            self.print_menu()

        if is_address(public_key) and (public_key == pk) and (private_key == check_private_key):

            print('Enter your personal account information.')
            print('(in this way every time you log in or want to perform a transaction it will not be necessary\n'
                  ' to provide your private key, but the username and password that you will specify below)')
            username = input('Username: ')

            while True:
                password = getpass.getpass('Password: ')
                check_password = getpass.getpass('Confirm Passoword: ')

                if not re.fullmatch(r'(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z0-9@#$%^&+=]{10,255}', password):
                    print(password)
                    print('Password must contains at least 10 symbols, at least one digit, at least one uppercase '
                          'letter, at least one lowercase letter.\n')
                elif password != check_password:
                    print('Password and confirm password do not match.\n')
                else:
                    break

            res = self.controller.register(username, password, public_key, private_key)
            if res == 0:
                print('Registration was successful!\n')
            elif res == -1:
                print('Username already present in the database.\n')
            elif res == -2:
                print('Sorry, but something went wrong!\n')

        else:
            print('Sorry, but the specified public key and private key do not match any account.\n')
            self.print_menu()

    def login_menu(self):

        if not self.controller.check_number_attempts() and self.session.get_time_left_for_unlock() < 0:
            self.session.reset_attempts()

        if self.session.get_time_left_for_unlock() <= 0 and self.controller.check_number_attempts():
            public_key = input('Public Key: ')
            private_key = input('Private Key: ')
            # private_key = getpass.getpass('Private Key: ')
            username = input('Username: ')
            password = getpass.getpass('Password: ')
            #res = self.controller.login(username, password, public_key, private_key)
            res = self.controller.login(username, password, public_key, private_key)

            if res == 0:
                print('\nYou are logged in.\n')
                self.print_user_options()
                return
                #if self.controller.check_password_obsolete(username):
                    #res= self.suggest_change_password(username)
                    #if res == 0:
                        #print('Password succesfully changed.\n')
                        #self.print_user_options()
                   #elif res == -1:
                        #print('Password not changed.\n')
                        #self.print_user_options()

            elif res == -1:
                print('\nIncorrect username or password\n')
                self.print_retry_exit_menu()
            elif res == -2:
                print('You have reached the maximum number of login attempts')
                return
        else:
            print('\nYou have reached the maximum number of attempts')
            print(f'Time left until next attempt: {int(self.session.get_time_left_for_unlock())} seconds\n')
            return

    def suggest_change_password(self, username):
        while True:
            response = input('It\'s been 3 months since your password was last changed. We suggest you change it.\n'
                  'Do you want to change your password (Y/N)?\n')
            if response == 'Y' or response == 'y':
                old_password = getpass.getpass('Old password: ')

                while True:
                    new_password = getpass.getpass('New password: ')
                    check_password = getpass.getpass('Confirm new passoword: ')

                    if not re.fullmatch(r'(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z0-9@#$%^&+=]{10,255}', new_password):
                        print(new_password)
                        print('Password must contains at least 10 symbols, at least one digit, at least one uppercase '
                              'letter, at least one lowercase letter.\n')
                    elif new_password != check_password:
                        print('Password and confirm password do not match.\n')
                    else:
                        break

                self.controller.change_password(username, new_password, old_password)
                return 0
            elif response == 'N' or response == 'n':
                return -1
            else:
                print('Wrong input.\n')


    def print_retry_exit_menu(self):
        for key in self.wrong_input_options.keys():
            print(key, '--', self.wrong_input_options[key])

        try:
            option = int(input('Enter your choice: '))
            if option == 1:
                print('\nHandle option \'Option 1: Retry\'')
                self.login_menu()

            elif option == 2:
                print('\nHandle option \'Option 2: Exit\'\n')
                self.print_menu()
            else:
                print('Invalid option. Please enter a number between 1 and 2.\n')
                self.print_retry_exit_menu()
        except ValueError:
            print('Wrong input. Please enter a number ...\n')
            self.print_retry_exit_menu()

    def print_user_options(self):
        for key in self.user_options.keys():
            print(key, '--', self.user_options[key])

        try:
            option = int(input('Enter your choice: '))
            if option == 1:
                print('\nHandle option \'Option 1: Deploy Smart Contract.\'')
                self.deploy_menu()
            elif option == 2:
                print('\nHandle option \'Option 2: Invoke Smart Contract\' Method.\'')
                self.invoke_method_menu()
            elif option == 3:
                print('\nHandle option \'Option 3:Consult your Smart Contract in your local databese.\'\n')
                self.print_smart_contract_deployed()
                self.print_user_options()
            elif option == 4:
                print('\nHandle option \'Option 4: Delete Smart Contract from your local databese.\'\n')
                self.delete_smart_contract_deployed()
            elif option == 5:
                print('\nHandle option \'Option 5: Logout.\'\n')
                self.session.set_user(None)
                self.print_menu()
            else:
                print('Invalid option. Please enter a number between 1 and 4.\n')
        except ValueError:
            print('Wrong input. Please enter a number ...\n')
            self.print_user_options()

    def deploy_menu(self):
        print('Before proceeding with the deployment of Smart Contract it is necessary to enter the password.')
        password = getpass.getpass('Password: ')
        res = self.controller.check_password(self.session.get_user().get_username(), password)
        if res:
            while True:
                file_path = self.read_smart_contract()
                if file_path:
                    break

            smart_contract_name = input('Smart Contract Name: ')

            while True:
                try:
                    gas_limit = int(input('Gas limit: '))
                    break
                except ValueError:
                    print('Wrong input. Please enter a number ...\n')

            while True:
                try:
                    gas_price = int(input('Gas price: '))
                    break
                except ValueError:
                    print('Wrong input. Please enter a number ...\n')

            estemate_cost = self.shards_controller.estimate(file_path, gas_limit, gas_price,
                                                            self.session.get_user().get_public_key())
            if estemate_cost == -1:
                print('Your gas limit is too low.\n')
                self.print_user_options()
            elif estemate_cost == -2:
                print('An unknown error occurred.\n')
                self.print_user_options()
            else:
                print(f'The estimated cost to deploy the smart contract is {str(estemate_cost)}.\n')
                while True:
                    print('Do you want proceed with the deploy (Y/N)?')
                    response = input('')
                    if response == 'Y' or response == 'y':
                        try:
                            res, shard = self.shards_controller.deploy_smart_contract(file_path, gas_limit, gas_price,
                                                                                  self.session.get_user().get_public_key())
                        except ContractLogicError:
                            print('Your Smart Conract has genereted logic error.\n')
                            self.print_user_options()
                            return
                        except Exception:
                            print('An unknown error occurred.\n')
                            self.print_user_options()
                            return
                        if res == -1:
                            print('Your gas limit is too low\n')
                            self.print_user_options()
                            break
                        elif res == -2:
                            print('Deployement failed\n')
                            self.print_user_options()
                            break
                        else:
                            print('Deployement was successful\n')
                            print(f'Contract deployed at address: {str(res)}.\n')
                            print(f'Shard address: {str(shard)}.\n')
                            self.controller.insert_smart_contract(smart_contract_name, res, shard,
                                                                  self.session.get_user())
                            self.print_user_options()
                            break

                    elif response == 'N' or response == 'n':
                        print('Transaction cancelled\n')
                        self.print_user_options()
                        break
                    else:
                        print('Wrong input.\n')

        else:
            print('\nIncorrect password.\n Sorry but you can\'t proceed with the deployment of Smart Contract.\n')
            self.print_user_options()

    def read_smart_contract(self):
        file_path = input('Enter the path of your file: ')
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            print(f'I did not find the file at {str(file_path)}.\n')
            return False
        elif not file_path.endswith('.sol'):
            print('File extension must be .sol')
            return False
        else:
            print('We found your file: Smart Contract loaded correctly!\n')
            return file_path

    def invoke_method_menu(self):
        print('Before proceeding with the invocation of a method of a smart contract it is necessary to enter the '
              'password.')
        password = getpass.getpass('Password: ')
        res = self.controller.check_password(self.session.get_user().get_username(), password)
        if res:
            while True:
                file_path = self.read_smart_contract()
                if file_path:
                    break

            while True:
                smart_contract_address = input('Enter smart contact address:')
                if is_address(smart_contract_address):
                    break
                elif not (is_address(smart_contract_address)):
                    print('Invalid smart contract address. Retry.\n')

            while True:
                shard = input('Enter shard address:')
                if shard in self.shards_controller.get_shards():
                    break
                elif shard not in self.shards_controller.get_shards():
                    print('Invalid shard address. Retry.\n')

            try:
                list_methods, contract, functions, web3 = self.shards_controller.smart_contract_methods_by_sourcecode(
                    shard,
                    smart_contract_address,
                    file_path)
            except:
                print('An unknown error occurred.\n')
                self.print_user_options()

            choice = self.print_smart_contract_methods(list_methods, contract)
            if choice == 0:
                self.print_user_options()
            else:
                parameters = self.print_parameters_methods(list_methods[choice - 1], web3)
                if parameters != -1:
                    invoked_function = ''
                    invoked_function += str(functions[choice-1]+'(')
                    if len(parameters) == 0:
                        invoked_function += ')'
                    else:
                        for i in range(0, len(parameters)):
                            invoked_function += str(parameters[i])
                            if i == len(parameters)-1:
                                invoked_function += ')'
                            else:
                                invoked_function += ','

                    if contract.abi[choice - 1]['stateMutability'] == 'view':
                        print('The function you wish to invoke is: ' + Fore.BLUE + str(invoked_function)
                              + Style.RESET_ALL)
                    else:
                        print('The function you wish to invoke is: ' + Fore.RED + str(invoked_function)
                              + Style.RESET_ALL)
                    while True:
                        answer = input('Would you like to continue? (Y/N)')
                        try:
                            if answer == 'Y' or answer == 'y':
                                res = self.shards_controller.call_function(functions[choice - 1],
                                                     choice - 1, parameters, contract,
                                                     self.session.get_user().get_public_key())
                                print(f'Result: {str(res)}.\n')
                                self.print_user_options()
                            if answer == 'N' or answer == 'n':
                                print('Execution Reverted.\n')
                                self.print_user_options()
                        except InvalidAddress:
                            print('The specified address is not valid.\n')
                        except ValidationError:
                            print('Function invocation failed due to no matching argument types.\n')
                        except Exception:
                            print('An unknown error occurred.\n')
                else:
                    print("Execution reverted due to wrong parameters")
                    self.print_user_options()
        else:
            print('\nIncorrect password.\n Sorry but you can\'t proceed with invocation of a method of a smart '
                  'contract.\n')
            self.print_user_options()

    def print_smart_contract_methods(self, list_methods: list, contract):
        n = 0
        for i in list_methods:
            n = n + 1
            if contract.abi[n-1]['stateMutability'] == 'view':
                print(Fore.BLUE + f'{str(n)}) {str(i)}{Style.RESET_ALL}')
            else:
                print(Fore.RED + f'{str(n)}) {str(i)}{Style.RESET_ALL}')

        while True:
            try:
                choice = int(input('Which of these methods do you want to invoke (press 0 to exit)? '))
                if choice < 0 or choice > n:
                    print('No option correspond to your choice. Retry.\n')
                elif choice == 0:
                    return 0
                else:
                    return choice
            except ValueError:
                print(f'Wrong input. Please enter a number between 1 and {str(n)}.\n')

    def print_parameters_methods(self, method: str, web3: str):
        parameters = method.replace(')', '').split('(')
        p = []
        n = 0
        parameters.pop(0)
        if parameters != ['']:
            for i in parameters:
                try:
                    n = n + 1
                    if not str(i).__contains__('['):
                        param = input(f'Parameter {str(n)} (type {str(i)}): ')
                        if str(i).startswith('bool'):
                            if param == 'true' or param == 'True' or param == '1':
                                p.append(True)
                            elif param == 'false' or param == 'False' or param == '0':
                                p.append(False)
                        elif str(i).startswith('int') or str(i).startswith('uint'):
                            p.append(web3.to_int(text=param))
                        elif str(i).startswith('fixed') or str(i).startswith('unfixed'):
                            p.append(float(i))
                        elif str(i).startswith('bytes'):
                            p.append(web3.to_bytes(text=param))
                    else:
                        list = self.retrieve_list_values()
                        casted_list = []
                        if str(i).startswith('bool'):
                            for i in range(0, len(list)):
                                if list[i] == 'true' or list[i] == 'True' or list[i] == '1':
                                    casted_list.append(True)
                                elif list[i] == 'false' or list[i] == 'False' or list[i] == '0':
                                    casted_list.append(False)
                            p.append(casted_list)
                        elif str(i).startswith('int') or str(i).startswith('uint'):
                            for i in range(0, len(list)):
                                casted_list.append(web3.to_int(text=list[i]))
                            p.append(casted_list)
                        elif str(i).startswith('fixed') or str(i).startswith('unfixed'):
                            for i in range(0, len(list)):
                                casted_list.append(float(list[i]))
                            p.append(casted_list)
                        elif str(i).startswith('bytes'):
                            for i in range(0, len(list)):
                                casted_list.append(web3.to_bytes(text=list[i]))
                            p.append(casted_list)
                    return p
                except:
                    return -1
        else:
            return p

    def print_smart_contract_deployed(self):
        smart_contract = self.session.get_user().get_smart_contracts()
        if len(smart_contract) == 0:
            print('No Smart Contracts deployed yet.\n')
        else:
            n = 1
            for contract in smart_contract:
                print(f'{str(n)} ---------------------------------------------------------------')
                print(f'Contract name: {str(contract.get_name())}')
                print(f'Contract address: {str(contract.get_address())}')
                print(f'Shard address: {str(contract.get_shard())}\n')
                n = n + 1

    def delete_smart_contract_deployed(self):
        smart_contract = self.session.get_user().get_smart_contracts()
        if len(smart_contract) == 0:
            print('No Smart Contracts deployed yet.\n')
            self.print_user_options()
        else:
            self.print_smart_contract_deployed()
            res = self.choose_smart_contract_to_delete(smart_contract)
            if res == 0:
                print('Successful delition.\n')
                self.print_user_options()
            elif res == -1:
                print('Sorry, but something went wrong with the delition!\n')
                self.print_user_options()
            elif res == -2:
                print('No Smart Contract delited.\n')
                self.print_user_options()

    def choose_smart_contract_to_delete(self, smart_contract: list):
        while True:
            try:
                choice = int(input('Which one do you want to delete from yor local database (press 0 to exit)? '))
                break
            except ValueError:
                print('Wrong input. Please enter a number ...\n')

        if choice < 0 or choice >= len(smart_contract) + 1:
            print('No option correspond to your choice. Retry.\n')
        elif choice == 0:
            return -2
        else:
            print('Smart Contract selected:')
            print(f'Contract name: {str(smart_contract[choice - 1].get_name())}')
            print(f'Contract address: {str(smart_contract[choice - 1].get_address())}')
            print(f'Shard address: {str(smart_contract[choice - 1].get_shard())}\n')
            while True:
                print('Do you want proceed with the delition (Y/N)?')
                response = input('')
                if response == 'Y' or response == 'y':
                    res = self.controller.delete_smart_contract(smart_contract[choice - 1])
                    return res
                elif response == 'N' or response == 'n':
                    return -2
                else:
                    print('Wrong input.\n')

    def retrieve_list_values(self):
        print('Choose list values, press enter to stop choosing values.')
        list = []
        while True:
            list_value = input('Value: ')
            if list_value != '':
                list.append(list_value)
            else:
                break
        return list

