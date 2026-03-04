import socket
import threading
from queue import Queue
from datetime import datetime

# Queue to store ports
port_queue = Queue()

# Number of threads
THREADS = 100

# Function to resolve domain to IP
def resolve_target(target):
    try:
        ip = socket.gethostbyname(target)
        print(f"[+] Target resolved: {target} -> {ip}")
        return ip
    except socket.gaierror:
        print("[!] Error: Unable to resolve hostname")
        exit()

# Function to scan a single port
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((ip, port))

        if result == 0:
            try:
                banner = sock.recv(1024).decode().strip()
            except:
                banner = "No banner"

            print(f"[OPEN] Port {port} | Service: {banner}")

        sock.close()

    except Exception:
        pass

# Worker thread function
def worker(ip):
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(ip, port)
        port_queue.task_done()

# Main function
def main():

    target = input("Enter target domain or IP: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))

    ip = resolve_target(target)

    print("\n[+] Starting scan...")
    print(f"[+] Scanning ports {start_port} - {end_port}")
    print("-" * 50)

    start_time = datetime.now()

    # Add ports to queue
    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    # Create threads
    for _ in range(THREADS):
        thread = threading.Thread(target=worker, args=(ip,))
        thread.start()

    port_queue.join()

    end_time = datetime.now()
    duration = end_time - start_time

    print("-" * 50)
    print(f"[+] Scan completed in: {duration}")

if __name__ == "__main__":
    main()
