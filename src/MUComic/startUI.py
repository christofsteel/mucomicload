from MUComic import UI
from MUComic.Qt.models import IssueModel, SeriesModel
from MUComic.Qt.threads import PopulateThread, DownloadThread
import sys
from PySide import QtGui, QtCore


class UIStarter():
	def populateIssueModel(self, series):
		# If we have an old populate Thread, kill it
		if hasattr(self,'populateThread') and self.populateThread.isRunning():
			self.populateThread.abort()
			self.populateThread.wait()

		self.issueModel = IssueModel(self.ui.listIssues)
		self.ui.listIssues.setModel(self.issueModel)
		self.populateThread = PopulateThread(self.issueModel, series, self.conn)
		self.populateThread.start()
		
	def changeHeader(self, i):
		self.ui.menuFile.setTitle(str(i))
	def updateIssues(self, item):
		series = item.data(QtCore.Qt.UserRole)
		self.populateIssueModel(series)
	
	def __init__(self, conn):
		self.conn = conn
		self.app = QtGui.QApplication(sys.argv)
		self.mw = QtGui.QMainWindow()
		self.ui = UI.Ui_MainWindow()
		self.ui.setupUi(self.mw)
	
	def start(self):
		self.seriesmodel = SeriesModel(self.conn.get_faved_series(), self.ui.listComics)

		firstIndex = self.seriesmodel.index(0,0)
		firstseries = (self.seriesmodel.data(firstIndex,QtCore.Qt.UserRole))

		self.issuemodel = self.populateIssueModel(firstseries)

		self.ui.listComics.setModel(self.seriesmodel)
		self.ui.listComics.clicked.connect(self.updateIssues)
		self.ui.listIssues.setModel(self.issuemodel)

		updateThread = DownloadThread() 
		updateThread.downloadingSignal.sig.connect(self.changeHeader)
		self.ui.actionUpdate.triggered.connect(updateThread.start)

		self.mw.show()
		sys.exit(self.app.exec_())
