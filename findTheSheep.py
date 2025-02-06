#!/usr/bin/env python3
# quick and dirty sheep finder

import socket
import ipaddress
import threading
import queue
import argparse
from datetime import datetime
import os
import sys
import time

class NetworkScanner:
    def __init__(self, subnet, output_file, num_threads=50, timeout=1):
        self.subnet = ipaddress.ip_network(subnet)
        self.output_file = output_file
        self.num_threads = num_threads
        self.timeout = timeout
        self.queue = queue.Queue()
        self.results = []
        self.lock = threading.Lock()
        self.active_hosts = 0
        
    def worker(self):
        while True:
            try:
                ip = self.queue.get_nowait()
            except queue.Empty:
                break
                
            try:
                # Check if host is up using TCP connection to port 80
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                result = sock.connect_ex((str(ip), 80))
                sock.close()
                
                if result == 0 or self.ping_host(str(ip)):
                    ports = self.scan_ports(ip)
                    if ports:
                        with self.lock:
                            self.results.append((str(ip), ports))
                            self.active_hosts += 1
                            print(f"Found open ports on {ip}")
            except:
                pass
                
            self.queue.task_done()

    def ping_host(self, ip):
        """Use system ping to check if host is up"""
        response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")
        return response == 0
    
    def scan_ports(self, ip):
        """Scan ports 1-1024 on a given IP"""
        open_ports = []
        
        for port in range(1, 1025):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            try:
                result = sock.connect_ex((str(ip), port))
                if result == 0:
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"
                    open_ports.append((port, service))
            except:
                pass
            finally:
                sock.close()
                
        return open_ports if open_ports else None

    def scan(self):
        start_time = time.time()
        print(f"Starting scan of {self.subnet} at {datetime.now()}")
        print("This may take several minutes depending on the subnet size, you cant rush perfection...")
        
        # Fill queue with IPs
        for ip in self.subnet.hosts():
            self.queue.put(ip)
            
        # Start worker threads
        threads = []
        for _ in range(min(self.num_threads, self.queue.qsize())):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)
            
        # Wait for scan completion
        for t in threads:
            t.join()
            
        # Sort results by IP
        self.results.sort(key=lambda x: int(ipaddress.IPv4Address(x[0])))
        
        # Write results to file
        with open(self.output_file, 'w') as f:
            f.write(f"Network Scan Results - {datetime.now()}\n")
            f.write(f"Subnet scanned: {self.subnet}\n")
            f.write(f"Scan duration: {time.time() - start_time:.2f} seconds\n")
            f.write(f"Active hosts found: {self.active_hosts}\n")
            f.write("=" * 50 + "\n\n")
            
            for ip, ports in self.results:
                f.write(f"\nHost: {ip}\n")
                f.write("-" * 20 + "\n")
                for port, service in sorted(ports):
                    f.write(f"Port: {port}\tService: {service}\n")
                    
        print(f"\nScan complete! Found {self.active_hosts} active hosts.")
        print(f"Results saved to {self.output_file}")

def main():
    parser = argparse.ArgumentParser(description='Network subnet scanner for Ubuntu 22.04')
    parser.add_argument('subnet', help='Subnet to scan (e.g., 192.168.1.0/24)')
    parser.add_argument('--output', '-o', default='scan_results.txt',
                       help='Output file name (default: scan_results.txt)')
    parser.add_argument('--threads', '-t', type=int, default=50,
                       help='Number of scanning threads (default: 50)')
    parser.add_argument('--timeout', '-w', type=float, default=1.0,
                       help='Timeout in seconds for each connection attempt (default: 1.0)')

    args = parser.parse_args()

    try:
        # Check for root privileges
        if os.geteuid() != 0:
            print("This script requires root privileges. Please run with sudo.")
            sys.exit(1)

        # Validate subnet
        try:
            ipaddress.ip_network(args.subnet)
        except ValueError as e:
            print(f"Invalid subnet format: {str(e)}")
            sys.exit(1)

        scanner = NetworkScanner(args.subnet, args.output, args.threads, args.timeout)
        scanner.scan()
        
    except KeyboardInterrupt:
        print("\nScan interrupted by user. Partial results may have been saved.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
