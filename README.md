# Simple Port Scanner (Python)

A basic TCP connect port scanner written in Python using the built-in `socket` module.  
This project is made for learning how port scanning works at a low level.

---

## 🔹 What it does
- Takes a target domain or IP
- Scans a given port range
- Prints only open ports
- Uses socket timeouts to avoid freezing

---

## 🔹 How it works
For each port:
- Create a socket
- Set a timeout
- Try to connect
- If connection succeeds → port is OPEN
- If it fails → move to next port

---

## 🔹 Requirements
- Python 3.x
- No external libraries
