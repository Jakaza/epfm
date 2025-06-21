import argparse
import os
from logger import log_action
from key_manager import get_fernet
from metadata_manager import add_metadata
from auth import verify_password

VAULT_DIR = "vault"
LOGS_DIR = "logs"
DATA_DIR = "data"
RECOVERED_DIR = "recovered"

def init():
    """Initialize the directory structure"""
    os.makedirs(VAULT_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    print("EPFM initialized successfully!")

def add_file(filename):
    fernet = get_fernet()

    if not os.path.exists(filename):
        print("File does not exist!")
        log_action("add", filename, "fail", "File not found")
        return

    try:
        with open(filename, "rb") as f:
            original = f.read()
            encrypted = fernet.encrypt(original)

        encrypted_filename = os.path.join(VAULT_DIR, os.path.basename(filename) + ".enc")
        with open(encrypted_filename, "wb") as f:
            f.write(encrypted)

        add_metadata(filename, encrypted_filename, original)
        log_action("add", filename, "success", "File not found")
        
    except Exception as ex:
        print(ex)
        log_action("add", filename, "fail", str(ex))


os.makedirs(RECOVERED_DIR, exist_ok=True)

def get_file(filename):
    fernet = get_fernet()
    enc_filename = os.path.join(VAULT_DIR, filename + ".enc")

    if not os.path.exists(enc_filename):
        log_action("get", filename, "fail", "Encrypted file not found in vault.")
        print("Encrypted file not found in vault.")
        return
    
    with open(enc_filename, "rb") as f:
        encrypted_data = f.read()

    try:
        decrypted_data = fernet.decrypt(encrypted_data)

        log_action("get", filename, "success", "Encrypted file was found in vault.")
    except Exception as ex:
        print(f"Failed to decrypt: {ex}")
        log_action("get", filename, "fail" , str(ex))
        return

    recovered_path = os.path.join(RECOVERED_DIR, filename)

    with open(recovered_path , "wb") as f:
        f.write(decrypted_data)

    print(f"File '{filename}' recovered and saved to '{recovered_path}'")

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
        if verify_password():
            add_file(args.filename)
    elif args.command == "get":
        if verify_password():
            get_file(args.filename)
    else:
        print("❗ Unknown command. Use --help to see options.")
        