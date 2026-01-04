import socket 
import threading
from queue import Queue

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


def scan_port():

    try:
        while not port_queue.empty():
            port = port_queue.get()
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    # one socket per port
            s.settimeout(TIMEOUT)
            result = s.connect_ex((target,port))
            if(result == 0):
                banner = ""
                try:
                    banner = s.recv(1024).decode(errors="ignore").strip()
                
                except:
                    pass

                result_line = f"[OPEN] {port}"
            
                if port in HTTP_PORTS: # Active HTTP detection
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

                elif banner:
                    result_line += f" | {banner}"

                with lock:
                    print(result_line)
                    with open(output_file, "a") as f:
                        f.write(result_line + "\n")

            s.close()
            port_queue.task_done() #  Tells queue that this port is fully processed
    except:
        pass
        

# ------ THREAD POOL ------

threads = []

for _ in range(THREAD_COUNT):   # Threads are created once and reused automatically
    t = threading.Thread(target=scan_port)
    t.start()
    threads.append(t)


port_queue.join() #  Main thread waits untill all ports are scanned


try:
    scan_port()

except KeyboardInterrupt:
    print("\n Scan stopped by user")

print("Scan completed.")