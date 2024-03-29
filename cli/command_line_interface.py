import os
import re

from colorama import Fore, Style
from eth_utils import is_address, decode_hex, ValidationError
from web3.exceptions import ContractLogicError, InvalidAddress

from controllers.controller import Controller
from controllers.shards_controller import ShardsController
from session.session import Session
from eth_keys import keys
from config import config

import getpass


class CommandLineInterface:

    def __init__(self, session: Session):

        self.controller = Controller(session)
        self.shards_controller = ShardsController(session, self.get_application_parameters())
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
            3: 'Consult your Smart Contract in your local database.',
            4: 'Delete Smart Contract from your local database.',
            5: 'Change password.',
            6: 'Logout.'
        }

    def get_application_parameters(self):
        num_of_shards = config.config["shards_number"]
        try:
            if int(num_of_shards) > 8:
                return 8
            elif int(num_of_shards) <= 0:
                return 1
            else:
                return int(num_of_shards)
        except Exception:
            return 3

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
                res = self.login_menu()
                if res == 0:
                    self.print_user_options()
            elif option == 3:
                print('\nHandle option \'Option 3: Exit\'')
                exit()
            else:
                print('Invalid option. Please enter a number between 1 and 3.\n')
                return

        except ValueError:
            print('Wrong input. Please enter a number ...\n')
            return

    def register_menu(self):
        print('Enter your wallet information.')
        public_key = input('Public Key: ')

        while True:
            #private_key = input('Private Key: ')
            private_key = getpass.getpass('Private Key: ')
            #check_private_key = input('Confirm Private Key: ')
            check_private_key = getpass.getpass('Confirm Private Key: ')
            if private_key == check_private_key:
                break
            else:
                print('Private key and confirm private key do not match. Retry.\n')

        try:
            priv_key_bytes = decode_hex(private_key)
            priv_key = keys.PrivateKey(priv_key_bytes)
            pk = priv_key.public_key.to_checksum_address()
        except Exception:
            print('Sorry, but the specified public key and private key do not match any wallet.\n')
            return

        if is_address(public_key) and (public_key == pk):

            print('Enter your personal account information.')
            print('(in this way every time you log in or want to perform a transaction it will not be necessary\n'
                  ' to provide your private key, but the username and password that you will specify below)')
            username = input('Username: ')

            while True:
                password = getpass.getpass('Password: ')
                check_password = getpass.getpass('Confirm Password: ')

                if not re.fullmatch(r'(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z0-9@#$%^&+=]{10,255}', password):
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
            return

    def login_menu(self):

        if not self.controller.check_number_attempts() and self.session.get_time_left_for_unlock() < 0:
            self.session.reset_attempts()

        if self.session.get_time_left_for_unlock() <= 0 and self.controller.check_number_attempts():
            public_key = input('Public Key: ')
            #private_key = input('Private Key: ')
            private_key = getpass.getpass('Private Key: ')
            username = input('Username: ')
            password = getpass.getpass('Password: ')
            res = self.controller.login(username, password, public_key, private_key)

            if res == 0:
                print('\nYou are logged in.\n')
                if self.controller.check_password_obsolete(username, password):
                    print('It\'s been 3 months since your password was last changed. We suggest you change it.\n')
                    self.change_password(username)
                return 0

            elif res == -1:
                print('\nWrong credentials\n')
                self.print_retry_exit_menu()
            elif res == -2:
                print('You have reached the maximum number of login attempts')
                return -1
        else:
            print('\nYou have reached the maximum number of attempts')
            print(f'Time left until next attempt: {int(self.session.get_time_left_for_unlock())} seconds\n')
            return -2

    def change_password(self, username: str):
        while True:
            response = input('Do you want to change your password (Y/N)? ')
            if response == 'Y' or response == 'y':
                old_password = getpass.getpass('Old password: ')

                if not self.controller.check_password(username, old_password):
                    print('\nSubmitted incorrect old password.\n')
                else:
                    while True:
                        new_password = getpass.getpass('New password: ')
                        check_password = getpass.getpass('Confirm new password: ')

                        if not re.fullmatch(r'(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z0-9@#$%^&+=]{10,255}',
                                            new_password):
                            print(
                                'Password must contains at least 10 symbols, at least one digit, at least one uppercase '
                                'letter, at least one lowercase letter.\n')
                        elif new_password != check_password:
                            print('Password and confirm password do not match.\n')
                        else:
                            break

                    res = self.controller.change_password(username, new_password, old_password)
                    if res == 0:
                        print('\nPassword changed.\n')
                    elif res == -1 or res == -2:
                        print('\nSorry, but something went wrong with the password change!\n')
                return

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
                res = self.login_menu()
                if res == 0:
                    self.print_user_options()

            elif option == 2:
                print('\nHandle option \'Option 2: Exit\'\n')
                return
            else:
                print('Invalid option. Please enter a number between 1 and 2.\n')
                self.print_retry_exit_menu()
        except ValueError:
            print('Wrong input. Please enter a number ...\n')
            self.print_retry_exit_menu()

    def print_user_options(self):
        while True:
            print('MENU')
            for key in self.user_options.keys():
                print(key, '--', self.user_options[key])
            try:
                option = int(input('Enter your choice: '))
                if option == 1:
                    print('\nHandle option \'Option 1: Deploy Smart Contract.\'')
                    self.deploy_menu()
                elif option == 2:
                    print('\nHandle option \'Option 2: Invoke Smart Contract\'s Method.\'')
                    self.invoke_method_menu()
                elif option == 3:
                    print(
                        '\nHandle option \'Option 3: Consult your Smart Contract in your local database.\'\n')
                    self.print_smart_contract_deployed()
                elif option == 4:
                    print('\nHandle option \'Option 4: Delete Smart Contract from your local database.\'\n')
                    self.delete_smart_contract_deployed()
                elif option == 5:
                    print('\nHandle option \'Option 5: Change password\'\n')
                    res = self.change_password(self.session.get_user().get_username())
                    if res == 0:
                        print('Password successfully changed.\n')
                    elif res == -1:
                        print('Password not changed.\n')
                elif option == 6:
                    print('\nHandle option \'Option 6: Logout.\'\n')
                    self.session.set_user(None)
                    return
                else:
                    print('Invalid option. Please enter a number between 1 and 6.\n')
            except ValueError:
                print('Wrong input. Please enter a number ...\n')

    def deploy_menu(self):
        print('Before proceeding with the deployment of Smart Contract it is necessary to enter the password.')
        password = getpass.getpass('Password: ')
        res = self.controller.check_password(self.session.get_user().get_username(), password)
        if res:
            while True:
                file_path = self.read_smart_contract()
                if file_path == '0':
                    return
                elif file_path:
                    break

            smart_contract_name = input('Smart Contract Name: ')

            while True:
                try:
                    gas_limit = int(input('\nGas limit (in Gwei): '))
                    break
                except ValueError:
                    print('Wrong input. Please enter a number ...\n')

            while True:
                try:
                    gas_price = int(input('Gas price (in Gwei): '))
                    break
                except ValueError:
                    print('Wrong input. Please enter a number ...\n')

            try:
                has_params, w3, constructor_parameters = self.shards_controller.check_parameters(file_path)
            except:
                print('An unknown error occurred.\n')
                return
            if has_params == -1:
                attr = []
            if has_params == 1:
                constructor = 'constructor('
                if constructor_parameters != []:
                    j = 0
                    for i in constructor_parameters:
                        j = j+1
                        constructor = constructor + str(i)
                        if j == len(constructor_parameters):
                            constructor = constructor + ')'
                    print('\nThis smart contract requires parameters in constructor: ' + Fore.RED + str(constructor)
                          + Style.RESET_ALL)
                    attr = self.print_parameters_methods(constructor, w3)

            estimate_cost = self.shards_controller.estimate(file_path, attr, gas_limit, gas_price)
            if estimate_cost == -1:
                print('Your gas limit is too low.\n')
                return
            elif estimate_cost == -2:
                print('Execution reverted: base fee exceeds gas limit.\n')
                return
            else:
                print(f'The estimated cost to deploy the smart contract is {str(estimate_cost)}.\n')
                while True:
                    response = input('Do you want proceed with the deploy (Y/N)? ')
                    if response == 'Y' or response == 'y':
                        try:
                            res, shard = self.shards_controller.deploy_smart_contract(file_path, attr, gas_limit, gas_price,
                                                                                      self.session.get_user().get_public_key(),
                                                                                      password)
                        except ContractLogicError:
                            print('Your Smart Contract has generated logic error.\n')
                            return
                        except Exception:
                            print('An unknown error occurred.\n')
                            return

                        print('Deployment was successful\n')
                        print(f'Contract deployed at address: {str(res)}.\n')
                        print(f'Shard address: {str(shard)}.\n')
                        self.controller.insert_smart_contract(smart_contract_name, res, shard,
                                                              self.session.get_user())
                        return

                    elif response == 'N' or response == 'n':
                        print('Transaction cancelled\n')
                        return
                    else:
                        print('Wrong input.\n')

        else:
            print('\nIncorrect password.\nSorry but you can\'t proceed with the deployment of Smart Contract.\n')

    def read_smart_contract(self):
        file_path = input('\nEnter the path of your file (press 0 to go back): ')
        if file_path == '0':
            print('\n')
            return file_path
        elif not os.path.exists(file_path) or not os.path.isfile(file_path):
            print(f'I did not find the file at {str(file_path)}.\n')
            return False
        elif not file_path.endswith('.sol'):
            print('File extension must be .sol')
            return False
        else:
            print('We found your file: Smart Contract loaded correctly!\n')
            return file_path

    def invoke_method_menu(self):
        view = 0
        print('Before proceeding with the invocation of a method of a smart contract it is necessary to enter the '
              'password.')
        password = getpass.getpass('Password: ')
        res = self.controller.check_password(self.session.get_user().get_username(), password)
        if res:
            while True:
                file_path = self.read_smart_contract()
                if file_path == '0':
                    return
                elif file_path:
                    break

            while True:
                smart_contract_address = input('Enter smart contact address (press 0 to go back): ')
                if is_address(smart_contract_address):
                    break
                elif smart_contract_address == '0':
                    print('\n')
                    return
                elif not (is_address(smart_contract_address)):
                    print('Invalid smart contract address. Retry.\n')

            while True:
                shard = input('Enter shard address (press 0 to go back): ')
                if shard in self.shards_controller.get_shards():
                    break
                elif shard == '0':
                    return
                elif shard not in self.shards_controller.get_shards():
                    print('Invalid shard address. Retry.\n')

            try:
                list_methods, contract, functions, web3 = self.shards_controller.smart_contract_methods_by_sourcecode(
                    shard,
                    smart_contract_address,
                    file_path)
            except:
                if self.shards_controller.smart_contract_methods_by_sourcecode(shard,
                                                                               smart_contract_address,
                                                                               file_path) == -1:
                    print('The smart contract address or the shard address specified do not match '
                                  'any contract deployed on the blockchain.\n')
                    return
                else:
                    print('An unknown error occurred.\n')
                    return

            choice = self.print_smart_contract_methods(list_methods, contract)
            if choice != 0:
                parameters = self.print_parameters_methods(list_methods[choice - 1], web3)
                if parameters != -1:
                    invoked_function = ''
                    invoked_function += str(functions[choice - 1] + '(')
                    if len(parameters) == 0:
                        invoked_function += ')'
                    else:
                        for i in range(0, len(parameters)):
                            invoked_function += str(parameters[i])
                            if i == len(parameters) - 1:
                                invoked_function += ')'
                            else:
                                invoked_function += ','
                    for i in contract.abi:

                        if str(functions[choice-1].split('(')[0]).replace(" ", "") == str(i['name']).replace(" ", ""):
                            if i['stateMutability'] == 'view':
                                print('\nThe function you wish to invoke is: ' + Fore.BLUE + str(invoked_function)
                                      + Style.RESET_ALL)
                                view = 1
                            else:
                                print('\nThe function you wish to invoke is: ' + Fore.RED + str(invoked_function)
                                      + Style.RESET_ALL)
                                view = 0
                    while True:
                        answer = input('Would you like to continue (Y/N)? ')
                        try:
                            if answer == 'Y' or answer == 'y':
                                if view == 1:
                                    res = self.shards_controller.call_function(web3, functions[choice - 1],
                                                                               parameters, contract,
                                                                               self.session.get_user().get_public_key(),
                                                                               password, None, None, view)
                                    print(f'Result: {str(res)}.\n')
                                    return
                                else:
                                    while True:
                                        try:
                                            gas_limit = int(input('\nGas limit (in Gwei): '))
                                            break
                                        except ValueError:
                                            print('Wrong input. Please enter a number ...\n')
                                    while True:
                                        try:
                                            gas_price = int(input('Gas price (in Gwei): '))
                                            break
                                        except ValueError:
                                            print('Wrong input. Please enter a number ...\n')

                                    estimate_cost = self.shards_controller.estimate_methodcall(web3,
                                                                                               functions[choice - 1],
                                                                                               parameters, contract,
                                                                                               gas_limit, gas_price,
                                                                                               smart_contract_address)

                                    if estimate_cost != -1:
                                        print('The estimated cost of your transaction is: ' + str(estimate_cost) + '\n')
                                    else:
                                        print('Execution reverted: base fee exceeds gas limit.\n')
                                        return

                                    while True:
                                        asw = input('Would you like to continue (Y/N)? ')
                                        try:
                                            if asw == 'Y' or asw == 'y':
                                                res, events, event_names = self.shards_controller.call_function(web3,
                                                                                           functions[choice - 1], parameters,
                                                                                           contract,
                                                                                           self.session.get_user().get_public_key(),
                                                                                           password, gas_price,
                                                                                           gas_limit, view)
                                                print(f'Function called correctly, the transaction hash is:' + str(res['transactionHash']) + '.\n')

                                                if events != []:
                                                    print('Events from smart contract.')
                                                    for i in range(0, len(events)):
                                                        print(Fore.LIGHTYELLOW_EX + "Event: "+event_names[i]+"\n" + "\n".join("{0} {1}".format("- "+k+": ", v) for k, v in events[i].items())
                                                            + Style.RESET_ALL)
                                                    print('\n')
                                                return
                                            if asw == 'N' or asw == 'n':
                                                print('Execution Reverted.\n')
                                                return
                                        except InvalidAddress:
                                            print('The specified address is not valid.\n')
                                            return
                                        except ValidationError:
                                            print('Function invocation failed due to no matching argument types.\n')
                                            return
                                        except Exception:
                                            print('An unknown error occurred.\n')
                                            return
                            if answer == 'N' or answer == 'n':
                                print('Execution Reverted.\n')
                                return
                        except InvalidAddress:
                            print('The specified address is not valid.\n')
                            return
                        except ValidationError:
                            print('Function invocation failed due to no matching argument types.\n')
                            return
                        except ContractLogicError:
                            print('The smart contract address or the shard address specified do not match '
                                  'any contract deployed on the blockchain.\n')
                            return
                        except Exception:
                            print('An unknown error occurred.\n')
                            return
                else:
                    print("Execution reverted due to wrong parameters.\n")
        else:
            print('\nIncorrect password.\nSorry but you can\'t proceed with invocation of a method of a smart '
                  'contract.\n')

    def print_smart_contract_methods(self, list_methods: list, contract: object):
        n = 0
        print('\nSmart Contract Methods:')
        for i in list_methods:
            for j in contract.abi:
                if str(i.split('(')[0]).replace(" ", "") == str(j['name']).replace(" ", ""):
                    if 'stateMutability' in j:
                        n = n+1
                        if j['stateMutability'] == 'view':
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
        n = 0
        attributes = []
        parameters.pop(0)
        p = parameters[0].split(',')
        if p != ['']:
            for i in p:
                try:
                    n = n + 1
                    if not str(i).__contains__('['):
                        param = input(f'Parameter {str(n)} (type {str(i)}): ')
                        if str(i).startswith('bool'):
                            if param == 'true' or param == 'True' or param == '1':
                                attributes.append(True)
                            elif param == 'false' or param == 'False' or param == '0':
                                attributes.append(False)
                        elif str(i).startswith('int') or str(i).startswith('uint'):
                            attributes.append(web3.to_int(text=param))
                        elif str(i).startswith('fixed') or str(i).startswith('unfixed'):
                            attributes.append(float(i))
                        elif str(i).startswith('bytes'):
                            #attributes.append(param)
                            attributes.append(web3.to_hex(hexstr=param))
                        elif str(i).startswith('string') or str(i).startswith('address'):
                            attributes.append(param)

                    else:
                        list = self.retrieve_list_values()
                        casted_list = []
                        if str(i).startswith('bool'):
                            for i in range(0, len(list)):
                                if list[i] == 'true' or list[i] == 'True' or list[i] == '1':
                                    casted_list.append(True)
                                elif list[i] == 'false' or list[i] == 'False' or list[i] == '0':
                                    casted_list.append(False)
                            attributes.append(casted_list)
                        elif str(i).startswith('int') or str(i).startswith('uint'):
                            for i in range(0, len(list)):
                                casted_list.append(web3.to_int(text=list[i]))
                            attributes.append(casted_list)
                        elif str(i).startswith('fixed') or str(i).startswith('unfixed'):
                            for i in range(0, len(list)):
                                casted_list.append(float(list[i]))
                            attributes.append(casted_list)
                        elif str(i).startswith('bytes'):
                            for i in range(0, len(list)):
                                #casted_list.append(web3.to_bytes(text=list[i]))
                                casted_list.append(web3.to_hex(hexstr=list[i]))
                                #casted_list.append(web3.to_bytes(text=list[i]))
                            attributes.append(casted_list)
                        elif str(i).startswith('string') or str(i).startswith('address'):
                            for i in range(0, len(list)):
                                casted_list.append(list[i])
                            attributes.append(casted_list)

                except:
                    return -1
            return attributes
        else:
            return attributes

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
        else:
            self.print_smart_contract_deployed()
            res = self.choose_smart_contract_to_delete(smart_contract)
            if res == 0:
                print('Successful deletion.\n')
            elif res == -1:
                print('Sorry, but something went wrong with the deletion!\n')
            elif res == -2:
                print('No Smart Contract deleted.\n')

    def choose_smart_contract_to_delete(self, smart_contract: list):
        while True:
            try:
                choice = int(input('Which one do you want to delete from your local database (press 0 to exit)? '))
            except ValueError:
                print('Wrong input. Please enter a number ...\n')

            if choice < 0 or choice >= len(smart_contract) + 1:
                print('No option correspond to your choice. Retry.\n')
            elif choice == 0:
                return -2
            elif choice > 0 or choice <= len(smart_contract) + 1:
                print('Smart Contract selected:')
                print(f'Contract name: {str(smart_contract[choice - 1].get_name())}')
                print(f'Contract address: {str(smart_contract[choice - 1].get_address())}')
                print(f'Shard address: {str(smart_contract[choice - 1].get_shard())}\n')
                break

        while True:
            response = input('Do you want proceed with the deletion (Y/N)? ')
            if response == 'Y' or response == 'y':
                res = self.controller.delete_smart_contract(smart_contract[choice - 1])
                return res
            elif response == 'N' or response == 'n':
                return -2
            else:
                print('Wrong input.\n')

    def retrieve_list_values(self):
        print('Choose list values, press Enter to stop choosing values.')
        l = []
        while True:
            list_value = input('Value: ')
            if list_value != '':
                l.append(list_value)
            else:
                break
        return l
