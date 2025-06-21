from cryptography.fernet import Fernet
import os

KEY_FILE = "data/secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

