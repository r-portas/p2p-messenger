"""
	Messenger GUI
	(c) 2015 Roy Portas
"""
import sys
from message_protocol import InboundSocket, OutboundSocket
from threading import Thread
from PySide import QtGui
from mainwindow import Ui_MainWindow as MainWindow

class Main(QtGui.QMainWindow):
	def __init__(self):
		super(Main, self).__init__()
		self.ui = MainWindow()
		self.ui.setupUi(self)

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
		self.inbound = InboundSocket()
		self.thread = Thread(target=self.inbound.listen, args=(self.listWidget,))
		self.thread.start()

		self.show()

	def set_ip(self):
		"""Set the IP to send messages to"""
		text, ok = QtGui.QInputDialog.getText(self, "Input Dialog", "Enter IP Address")
		if ok:
			self.target_ip = text
			self.outbound = OutboundSocket()
			self.outbound.setTarget(self.target_ip)
			print("Setting target ip to {}".format(text))

	def set_name(self):
		"""Set the user's name"""
		text, ok = QtGui.QInputDialog.getText(self, "Input Dialog", "Enter Name")
		if ok:
			self.name = text
			print("Setting name to {}".format(text))

	def send(self):
		"""Send a message"""
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