import socket 
import threading
from queue import Queue
import ssl

THREAD_COUNT = 50
TIMEOUT = 2
HTTP_PORTS = {80, 8080, 8000}

target = input("Enter a Target(Domain name or IP): ")

stPort = int(input("Enter the starting port : "))

endPort = int(input("Enter the end port : "))

output_file = "scan_results.txt"
lock = threading.Lock()

# print("Trying to connect...")

port_queue = Queue()

for port in range(stPort, endPort+1):
    port_queue.put(port)


def detect_tls(sock, target):
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        tsl_sock = context.wrap_socket(sock, server_hostname=target)
        tsl_sock.close()
        return True
    
    except:
        return False

def detect_ssh(sock):
    try:
        banner = sock.recv(1024).decode(errors="ignore")#.strip()
        if banner.startswith("SSH"):
            return banner.strip()
    except:
        pass
    return None

def scan_port():

    try:
        # banner = ""
        while not port_queue.empty():
            port = port_queue.get()
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    # one socket per port
            s.settimeout(TIMEOUT)
            result = s.connect_ex((target,port))
            if(result == 0):
                result_line = f"[OPEN] {port}"
                ssh_banner = detect_ssh(s)
                if ssh_banner: # SSH Detection
                    result_line += f" | {ssh_banner}"
                else:
                    if port == 443: # TLS Detection for HTTPS port 
                        if detect_tls(s, target):
                            result_line += " | TLS Detected"
            
                    elif port in HTTP_PORTS: # Active HTTP detection
                        try:
                            request = f"HEAD / HTTP/1.1\r\nHost: {target}\r\n\r\n" #Head request 
                            s.send(request.encode())
                            response = s.recv(1024).decode(errors="ignore")

                            if response:    
                                first_line = response.splitlines()[0]
                                server_line = ""
                                for line in response.splitlines():  #looking for server line
                                    if line.lower().startswith("server"):
                                        server_line = line
                                        break

                                result_line += f" | HTTP | {first_line}"
                                if server_line:
                                    result_line += f" | {server_line}"
                        except:
                            pass

                # if banner:
                #     result_line += f" | {banner}"

                with lock:
                    print(result_line)
                    try:
                        with open(output_file, "a") as f:
                            f.write(result_line + "\n")
                            f.flush()  # Force write immediately
                    except Exception as e:
                        print(f"Error writing to file: {e}")

            s.close()
            port_queue.task_done() #  Tells queue that this port is fully processed
    except Exception as e: 
        print(f"Thread error: {e}")

# Open file once at the beginning
with open(output_file, "w") as f:
    f.write(f"Scan results for {target}\n")
    f.write("="*50 + "\n")
        
# ------ THREAD POOL ------

threads = []

for _ in range(THREAD_COUNT):   # Threads are created once and reused automatically
    t = threading.Thread(target=scan_port)
    t.daemon = True
    t.start()
    threads.append(t)

try:
    port_queue.join()  # This blocks until all ports processed
    print("Scan completed.")

except KeyboardInterrupt:
    print("\nScan interrupted by user.")
    # Clear queue to stop threads
    while not port_queue.empty():
        port_queue.get()
        port_queue.task_done()