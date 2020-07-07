from cryptography.fernet import Fernet
import sys
import os

# Key generation
cipher_suite = Fernet(os.environ['FERNET_KEY'].encode())

def encode(text: str) -> str:
    return cipher_suite.encrypt(text.encode()).decode('utf-8')

def decode(text: str) -> str:
    return cipher_suite.decrypt(text.encode()).decode('utf-8')