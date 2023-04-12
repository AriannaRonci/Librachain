from cli.command_line_interface import CommandLineInterface
from session.session import Session

if __name__ == "__main__":
    session_obj = Session()
    cli = CommandLineInterface(session_obj)
    while True:
        cli.print_menu()
