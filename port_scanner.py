import socket 


target = input("Enter a Domain Name : ")

stPort = int(input("Enter the starting port : "))

endPort = int(input("Enter the end port : "))

print("Trying to connect...")

for i in range (stPort,endPort+1):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((target,i))
        print(f" port-{i} is Open ")
        s.close()

    except:
        print(f" port {i} is closed")
        s.close()
        continue
