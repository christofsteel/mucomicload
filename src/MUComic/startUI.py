from MUComic import UI, settingsWindow
from MUComic.Qt.models import IssueModel, SeriesModel
from MUComic.Qt.threads import PopulateThread, UpdateFavedSeriesThread,DownloadThread
import sys
from PySide import QtGui, QtCore


class UIStarter():

	def updateFavedSeries(self):
		if hasattr(self,'updateThread') and self.updateThread.isRunning():
			self.updateThread.wait()
		else:
			self.updateThread = UpdateFavedSeriesThread(self.seriesmodel)
			self.updateThread.started.connect(lambda:self.ui.actionUpdate.setDisabled(True))
			self.updateThread.finished.connect(lambda:self.ui.actionUpdate.setDisabled(False))
			self.updateThread.terminated.connect(lambda:self.ui.actionUpdate.setDisabled(False))
			self.updateThread.start()

	def downloadIssue(self):
		issue = self.ui.listIssues.model().data(self.ui.listIssues.currentIndex(),QtCore.Qt.UserRole)
		downloadThread = DownloadThread(issue,self.conn,self.mw)
		downloadThread.start()

	def addSeries(self):
		series_id, ok = QtGui.QInputDialog.getInt(self.mw, "Add Series", "Enter Series ID")
		self.conn.db.set_series_fav(series_id, 1)
		self.updateSeriesModel()
	
	def updateSeriesModel(self):
		faved_series = self.conn.get_faved_series()
		self.seriesmodel.setDatas(faved_series)

	def populateIssueModel(self, series):
		# If we have an old populate Thread, kill it
		if hasattr(self,'populateThread') and self.populateThread.isRunning():
			self.populateThread.abort()
			self.populateThread.wait()

		self.issueModel = IssueModel(self.ui.listIssues)
		self.ui.listIssues.setModel(self.issueModel)
		self.populateThread = PopulateThread(self.issueModel, series, self.conn)
		self.populateThread.start()
		
	def updateIssuesModel(self, item):
		series = item.data(QtCore.Qt.UserRole)
		self.populateIssueModel(series)
	
	def __init__(self, conn):
		self.conn = conn
		self.app = QtGui.QApplication(sys.argv)
		self.mw = QtGui.QMainWindow()
		self.ui = UI.Ui_MainWindow()
		self.ui.setupUi(self.mw)
		self.ui.listIssues.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		self.ui.actionDownload.triggered.connect(self.downloadIssue)
		self.ui.listIssues.addAction(self.ui.actionDownload)

		self.settingswindow = settingsWindow.Ui_Form()
		self.settingswindowform = QtGui.QDialog()
		self.settingswindow.setupUi(self.settingswindowform)
		self.ui.menuFileSettings.triggered.connect(self.settingswindowform.show)
	
	def start(self):
		self.seriesmodel = SeriesModel(self.conn.get_faved_series(), self.conn, self.ui.listComics)

		firstIndex = self.seriesmodel.index(0,0)
		firstseries = (self.seriesmodel.data(firstIndex,QtCore.Qt.UserRole))

		self.issuemodel = self.populateIssueModel(firstseries)

		self.ui.listComics.setModel(self.seriesmodel)
		self.ui.listComics.clicked.connect(self.updateIssuesModel)
		self.ui.listIssues.setModel(self.issuemodel)

		self.ui.actionUpdate.triggered.connect(self.updateFavedSeries)
		self.ui.actionAdd_series.triggered.connect(self.addSeries)

		self.mw.show()
		sys.exit(self.app.exec_())
