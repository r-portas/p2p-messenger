"""
    Message protocol
    Contains the classes required to create a messenger object
    (c) 2015 Roy Portas
"""
import socket
from logging import warning, error
from threading import Thread

LISTENING_PORT = 1500

class InboundSocket():
    """The inbound socket listens for inbound messages"""
    def __init__(self, backlog=5, listwidget=None, ipaddress=None):
        global LISTENING_PORT
        self.port = LISTENING_PORT

        self.messages = [] # Store received messages
        self.maxMsgSize = 1024
        self.alive = 1 # Controls the server's state, set to 0 to close

        # Create a socket that communicates over IPv4 (AF_INET) via TCP (SOCK_STREAM)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set the socket so it is reusable
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.success = 0
        while self.success == 0:
            try:
                self.socket.bind(('', self.port))
                print("[+] Socket running on port {}".format(self.port))
                if listwidget:
                    listwidget.addItem("Chat server on {}:{}".format(ipaddress, self.port))
                self.success = 1
                break
            except:
                self.port += 1
        #Backlog indicates the number of messages to queue up
        self.socket.listen(backlog)

    def listen(self, listWidget=None):
        """Listen for inbound communication"""
        while self.alive:
            try:
                cSock, cAddr = self.socket.accept()
                cSock.settimeout(None)
                msg = self.retrieve_data(cSock, cAddr)
                print(msg)
                if listWidget:
                    listWidget.addItem(msg)
                #Thread(target=self.retrieve_data, args=(cSock, cAddr)).start()
            except Exception as e:
                error(e)
            
        self.socket.close()

        
    def close_server(self):
        """Closes the sever"""
        self.alive = 0

    def retrieve_data(self, inboundSocket, inboundAddress):
        """
        Retrieve data from a peer
        NOTE: Should be ran from within a thread
        """
        message = inboundSocket.recv(self.maxMsgSize)
        message = message.strip()
        message = message.decode()
        inboundSocket.close()
        self.messages.append(message)
        warning("Received from {}:{} : {}".format(inboundAddress[0],
            inboundAddress[1],
            message))
        return message


class OutboundSocket():
    """The outbound socket sends data"""
    def __init__(self):
        global LISTENING_PORT
        # Set the port to transmit from
        self.targetPort = LISTENING_PORT
        self.targetAddress = ""

    def set_target(self, hostIp, targetPort=None):
        """Sets the host ip address to send the data to"""
        self.targetAddress = hostIp
        if targetPort:
            self.targetPort = targetPort

    def send_message(self, msg):
        """Connect and send message to the target"""
        if self.targetAddress != "":
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Set the socket so it is reusable
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                sock.connect((self.targetAddress, self.targetPort))
                sock.sendall(msg.encode())
                sock.close()
            except Exception as e:
                error(e)
        else:
            error("Target ip address is not set")