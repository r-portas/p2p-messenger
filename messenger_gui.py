"""
	Messenger GUI
	(c) 2015 Roy Portas
"""
import sys
from message_protocol import InboundSocket, OutboundSocket
from threading import Thread
from PySide import QtGui
from mainwindow import Ui_MainWindow as MainWindow
from getip import get_ip

class Main(QtGui.QMainWindow):
	def __init__(self):
		super(Main, self).__init__()
		self.ui = MainWindow()
		self.ui.setupUi(self)
		self.ip = get_ip()

		#Window objects
		self.listWidget = self.ui.listWidget
		self.lineEdit = self.ui.lineEdit
		self.sendButton = self.ui.sendButton

		self.ui.actionConnect_to_user.triggered.connect(self.set_ip)
		self.ui.actionSet_name.triggered.connect(self.set_name)

		self.sendButton.clicked.connect(self.send)
		self.lineEdit.returnPressed.connect(self.send)

		self.name = "User"
		self.target_ip = "127.0.0.1"

		self.outbound = None
		self.inbound = InboundSocket(5, self.listWidget, self.ip)
		self.thread = Thread(target=self.inbound.listen, args=(self.listWidget,))
		self.thread.start()

		self.show()

	def set_ip(self):
		"""Set the IP to send messages to"""
		text, ok = QtGui.QInputDialog.getText(self, "Input Dialog", "Enter IP Address")
		if ok:
			self.outbound = OutboundSocket()
			if ':' in text:
				self.target_ip, port = text.split(":")
				self.outbound.set_target(self.target_ip, int(port))
			else:
				self.target_ip = text
				self.outbound.set_target(self.target_ip)
			
			# Send a message to other client saying that user connected
			if self.outbound != None:
				self.outbound.send_message("{} connected from IP {}".format(self.name, self.ip))

	def set_name(self):
		"""Set the user's name"""
		text, ok = QtGui.QInputDialog.getText(self, "Input Dialog", "Enter Name")
		if ok:
			nameChange = "{} has changed their name to {}".format(self.name, text)
			self.listWidget.addItem(nameChange)
			if self.outbound != None:
				self.outbound.send_message(nameChange)
			self.name = text
			print("Setting name to {}".format(text))

	def send(self):
		"""Send a message"""
		if self.lineEdit.text() != '':
			temp = "{}: {}".format(self.name, self.lineEdit.text())
			self.lineEdit.clear()
			self.listWidget.addItem(temp)

			if self.outbound != None:
				self.outbound.send_message(temp)

	#TODO: Shutdown the inbound socket once application closed

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	win = Main()
	sys.exit(app.exec_())