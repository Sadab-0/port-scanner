# 🔍 Python Multi-Threaded Port Scanner

A fast and lightweight **TCP port scanner** written in Python using multithreading and a queue-based worker model.  
The scanner detects open ports, performs **basic banner grabbing**, and identifies **HTTP services** on common HTTP ports.

This project is intended for **learning and understanding** how real port scanners work internally.

---

## ✨ Features

- Multi-threaded port scanning
- Queue-based worker architecture
- TCP connect scan using `connect_ex`
- Open port detection
- Basic banner grabbing
- Active HTTP service detection using `HEAD` requests
- Thread-safe console output
- Saves scan results to a file

---

## 🧠 How It Works

1. Ports are added to a shared queue  
2. A fixed pool of threads consumes ports from the queue  
3. Each thread:
   - Creates a socket
   - Attempts a TCP connection
   - Checks if the port is open
   - Grabs service banners (if available)
   - Performs HTTP detection on common HTTP ports
4. Results are printed and saved safely using a thread lock

---

## 🛠 Requirements

- Python 3.x  
- No external libraries (uses only the Python standard library)

---

## 🚀 Usage

Run the script:

```bash
python port_scanner.py