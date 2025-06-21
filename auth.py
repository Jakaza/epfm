import os
import json
import bcrypt
from getpass import getpass

AUTH_FILE = "data/auth.json"

def password_file_exist():
    return os.path.exists(AUTH_FILE)

def create_password():
    print("🔐 Set a master password for EPFM")
    while True:
        pw1 = getpass("Enter password: ")
        pw2 = getpass("Confirm password: ")
        if pw1 == pw2 :
            hashed = bcrypt.hashpw(pw1.encode(), bcrypt.gensalt()).decode()
            with open(AUTH_FILE, 'w') as f:
                json.dump({"password" : hashed}, f)
            print("Password set successfully.")
            return
        else:
             print("Password do not match.")
            

def verify_password():
    if not password_file_exist():
        create_password()

    with open(AUTH_FILE, 'r') as f:
        stored = json.load(f)["password"]

    for _ in range(5) :
        pw = getpass("Enter master password: ")
        if bcrypt.checkpw(pw.encode(), stored.encode()):
            print("Access granted.")
            return True
        else:
            print("Incorrect password.")

    print("Too many failed attempts.")
    return False

