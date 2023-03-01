import os
from cryptography.fernet import Fernet

def get_key_from_file():
    if os.path.exists('fernet.key'):
        with open('fernet.key', 'rb') as fkey:
            return fkey.read()
    else:
        with open('fernet.key', 'wb') as fkey:
            new_fkey = Fernet.generate_key()
            fkey.write(new_fkey)
            return new_fkey