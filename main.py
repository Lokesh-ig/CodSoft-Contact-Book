"""
Main Entry Point for Contact Book Application.
Run without arguments for GUI mode, or pass --cli for Command Line mode.
"""

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Contact Book Application")
    parser.add_argument("--cli", action="store_true", help="Launch in Command Line Interface mode")
    args = parser.parse_args()

    if args.cli:
        from cli_contact_book import ContactBookCLI
        app = ContactBookCLI()
        app.run()
    else:
        from contact_book_gui import main as gui_main
        gui_main()


if __name__ == "__main__":
    main()
