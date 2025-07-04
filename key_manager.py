from cryptography.fernet import Fernet
import os

KEY_FILE = "data/secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()
    
def get_fernet():
    key = load_key()
    return Fernet(key=key)


