from MUComic import UI, settingsWindow
from MUComic.Qt.models import IssueModel, SeriesModel
from MUComic.Qt.threads import PopulateThread, UpdateThread,DownloadThread
import sys
from PySide import QtGui, QtCore


class UIStarter():
	def notify(self, text):
		print(text)
		self.ui.statusBar.showMessage(text)

	def updateSeries(self):
		if hasattr(self,'updateThread') and self.updateThread.isRunning():
			self.updateThread.wait()
		else:
			self.updateThread = UpdateThread(self.seriesmodel)
			self.updateThread.started.connect(lambda:self.ui.actionUpdate.setDisabled(True))
			self.updateThread.finished.connect(lambda:self.ui.actionUpdate.setDisabled(False))
			self.updateThread.terminated.connect(lambda:self.ui.actionUpdate.setDisabled(False))
			self.updateThread.statusChanged.connect(self.notify)
			self.updateThread.start()

	def downloadIssue(self):
		if hasattr(self,'downloadThread') and self.downloadThread.isRunning():
			self.downloadThread.wait()
		else:
			issue = self.ui.listIssues.model().data(self.ui.listIssues.currentIndex(),QtCore.Qt.UserRole)
			self.downloadThread = DownloadThread(issue,self.conn,self.mw)
			self.downloadThread.started.connect(lambda:self.ui.actionDownload.setDisabled(True))
			self.downloadThread.statusChanged.connect(self.notify)
			self.downloadThread.finished.connect(lambda:self.ui.actionDownload.setDisabled(False))
			self.downloadThread.terminated.connect(lambda:self.ui.actionDownload.setDisabled(False))
			self.downloadThread.start()

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

	def updateConfig(self):
		self.conn.config.set("MUComicLoad","username",
				self.settingswindow.le_username.text())
		self.conn.config.set("MUComicLoad","password",
				self.settingswindow.le_passwd.text())
		self.conn.config.set("MUComicLoad","comicviewer",
				self.settingswindow.le_comicViewer.text())
		self.conn.config.set("MUComicLoad","downloaddir",
				self.settingswindow.le_download.text())
		self.conn.updateConfig()
		self.settingswindowform.close()

	def revertConfig(self):
		self.settingswindow.le_username.setText(self.conn.config['MUComicLoad']['username'])
		self.settingswindow.le_passwd.setText(self.conn.config['MUComicLoad']['password'])
		self.settingswindow.le_comicViewer.setText(self.conn.config['MUComicLoad']['comicviewer'])
		self.settingswindow.le_download.setText(self.conn.config['MUComicLoad']['downloaddir'])
		self.settingswindowform.close()

	
	def browseComicViewerClicked(self):
		comicViewer, snd = QtGui.QFileDialog.getOpenFileName()
		if comicViewer:
			self.settingswindow.le_comicViewer.setText(comicViewer)

	def browseDownloadDirClicked(self):
		downloadDir = QtGui.QFileDialog.getExistingDirectory()
		if downloadDir:
			self.settingswindow.le_download.setText(downloadDir)

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
		self.settingswindowform = QtGui.QDialog(self.mw)
		self.settingswindow.setupUi(self.settingswindowform)
		self.settingswindow.le_username.setText(self.conn.config['MUComicLoad']['username'])
		self.settingswindow.le_passwd.setText(self.conn.config['MUComicLoad']['password'])
		self.settingswindow.le_comicViewer.setText(self.conn.config['MUComicLoad']['comicviewer'])
		self.settingswindow.le_download.setText(self.conn.config['MUComicLoad']['downloaddir'])
		self.settingswindow.btn_comicViewer.clicked.connect(self.browseComicViewerClicked)
		self.settingswindow.btn_download.clicked.connect(self.browseDownloadDirClicked)
		self.settingswindow.buttonBox.accepted.connect(self.updateConfig)
		self.settingswindow.buttonBox.rejected.connect(self.revertConfig)

		self.ui.menuFileSettings.triggered.connect(self.settingswindowform.show)
	
	def start(self):
		self.seriesmodel = SeriesModel(self.conn.get_faved_series(), self.conn, self.ui.listComics)

		self.ui.listComics.setModel(self.seriesmodel)
		self.ui.listComics.clicked.connect(self.updateIssuesModel)

		self.issuemodel = IssueModel(self.ui.listIssues)
		if self.seriesmodel.rowCount(None) > 0:
			firstIndex = self.seriesmodel.index(0,0)
			firstseries = (self.seriesmodel.data(firstIndex,QtCore.Qt.UserRole))
			self.populateIssueModel(firstseries)


		self.ui.actionUpdate.triggered.connect(self.updateSeries)
		self.ui.actionAdd_series.triggered.connect(self.addSeries)

		self.mw.show()
		sys.exit(self.app.exec_())
