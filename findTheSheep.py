#!/usr/bin/env python3
import socket
from concurrent.futures import ThreadPoolExecutor

# Define the subnet and port range
SUBNET = '192.168.80.0/24'  # Change this to your subnet
PORT_START = 1
PORT_END = 1024

# Function to check if a port is open on a given IP address
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            return ip, port
        sock.close()
    except Exception as e:
        pass

# Function to scan a subnet for open ports
def scan_subnet(subnet):
    results = []
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, f"{subnet}{i}", port) for i in range(256) for port in range(PORT_START, PORT_END + 1)]
        
        for future in futures:
            result = future.result()
            if result:
                results.append(result)
    
    return results

# Function to save the open ports and IP addresses to a text file
def save_results(results):
    with open('open_ports.txt', 'w') as file:
        for ip, port in results:
            file.write(f"{ip}:{port}\n")

# Main function to execute the scan and save results
def main():
    print("Scanning subnet...")
    
    results = scan_subnet(SUBNET)
    
    if results:
        print(f"Found {len(results)} open ports:")
        for ip, port in results:
            print(f"{ip}:{port}")
        
        save_results(results)
        print("Scan complete. Results saved to 'open_ports.txt'.")
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()
