"""
	Messenger GUI
	(c) 2015 Roy Portas
"""
import sys
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

		self.show()

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	win = Main()
	sys.exit(app.exec_())