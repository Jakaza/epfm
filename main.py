import argparse
import os

VAULT_DIR = "vault"
LOGS_DIR = "logs"
DATA_DIR = "data"

def init():
    """Initialize the directory structure"""
    os.makedirs(VAULT_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    print("🔐 EPFM initialized successfully!")

def add_file(filename):
    print(f"[+] You selected to add file: {filename}")

def get_file(filename):
    print(f"[+] You selected to get file: {filename}")

def setup_cli():
    parser = argparse.ArgumentParser(description="Encrypted Personal File Manager (EPFM)")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("init", help="Initialize EPFM folders")

    parser_add = subparsers.add_parser("add", help="Add a file to the vault")
    parser_add.add_argument("filename", type=str, help="Path to the file")

    parser_get = subparsers.add_parser("get", help="Retrieve a file from the vault")
    parser_get.add_argument("filename", type=str, help="Name of the file to retrieve")

    return parser.parse_args()


if __name__ == "__main__":
    args = setup_cli()

    if args.command == "init":
        init()
    elif args.command == "add":
        add_file(args.filename)
    elif args.command == "get":
        get_file(args.filename)
    else:
        print("❗ Unknown command. Use --help to see options.")
        