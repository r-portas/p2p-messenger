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
    def __init__(self, backlog=5):
        global LISTENING_PORT
        self.port = LISTENING_PORT

        self.messages = [] # Store received messages
        self.maxMsgSize = 1024
        self.alive = 1 # Controls the server's state, set to 0 to close

        # Create a socket that communicates over IPv4 (AF_INET) via TCP (SOCK_STREAM)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set the socket so it is reusable
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket.bind(('', self.port))
        #Backlog indicates the number of messages to queue up
        self.socket.listen(backlog)
        self.listen()

    def listen(self):
        """Listen for inbound communication"""
        try:
            while self.alive:
                cSock, cAddr = self.socket.accept()
                cSock.settimeout(None)
                Thread(target=self.retrieve_data, args=(cSock, cAddr)).start()
            self.socket.close()

        except Exception as e:
            error(e)

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


class OutboundSocket():
    """The outbound socket sends data"""
    def __init__(self):
        global LISTENING_PORT
        # Set the port to transmit from
        self.targetPort = LISTENING_PORT
        self.targetAddress = ""

    def set_target(self, hostIp):
        """Sets the host ip address to send the data to"""
        self.targetAddress = hostIp

    def send_message(self, msg):
        """Connect and send message to the target"""
        if self.targetAddress != "":
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.targetAddress, self.targetPort))
                sock.sendall(msg.encode())
                sock.close()
            except Exception as e:
                error(e)
        else:
            error("Target ip address is not set")
