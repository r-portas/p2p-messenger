"""
Test server
Listens for messages and sends them back
(c) 2015 Roy Portas
"""

import socket

listen_port = 1604
send_port = 1500 #The default port for the chat program

print("[+] Listening for messages on port {}".format(listen_port))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", listen_port))
sock.listen(10)

while True:
    cSock, cAddr = sock.accept()
    message = cSock.recv(1000)
    message = message.strip()
    print(cAddr, message)

    # Send the message back
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((cAddr[0], send_port))
    s.sendall(message)
    s.close()