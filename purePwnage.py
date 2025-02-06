#!/usr/bin/env python3
#This is a simulation script to create a text file and then encrypt it. This could simulate a Ransoomware attack. The script also dumps a ransom note for the admin.
#Make sure cryptography is installed on the system
#If this is a new system, chmod the file: chmod +x purePwnage.py

import os
from cryptography.fernet import Fernet
from datetime import datetime

# Define the plain text file and encrypted file names
PLAIN_TEXT_FILE = 'plain_text.txt'
ENCRYPTED_FILE = f'{PLAIN_TEXT_FILE}.encrypt'
METADATA_FILE = 'encryption_metadata.txt'

# Function to generate a key for encryption
def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Function to load the key from the current directory named `secret.key`
def load_key():
    """
    Load the previously generated key
    """
    return open("secret.key", "rb").read()

# Function to encrypt a file
def encrypt_file(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(ENCRYPTED_FILE, "wb") as file:
        file.write(encrypted_data)

# Function to create metadata file
def create_metadata_file():
    """
    Create a text file containing metadata about the encryption process
    """
    with open(METADATA_FILE, 'w') as metadata_file:
        metadata_file.write("Metadata for Encryption Process\n")
        metadata_file.write(f"File Name: {PLAIN_TEXT_FILE}\n")
        metadata_file.write(f"Encrypted File Name: {ENCRYPTED_FILE}\n")
        metadata_file.write(f"Encryption Time: {datetime.now()}\n")

# Main function to handle the encryption process
def main():
    # Generate and load key
    generate_key()
    key = load_key()

    # Create plain text file
    with open(PLAIN_TEXT_FILE, 'w') as file:
        file.write("This is a plain text file for encryption.")

    # Encrypt the plain text file
    encrypt_file(PLAIN_TEXT_FILE, key)

    # Create metadata file
    create_metadata_file()

    print(f"Plain Text File: {PLAIN_TEXT_FILE}")
    print(f"Encrypted File: {ENCRYPTED_FILE}")
    print(f"Metadata File: {METADATA_FILE}")

if __name__ == "__main__":
    main()
