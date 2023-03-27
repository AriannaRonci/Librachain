from cli.CommandLineInterface import CommandLineInterface
from controller.Controller import Controller

if __name__ == "__main__":
    cli = CommandLineInterface()
    while (True):
        cli.print_menu()