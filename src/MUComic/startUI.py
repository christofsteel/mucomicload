from MUComic import UI, settingsWindow, SearchWindow
from MUComic.Qt.models import IssueModel, SeriesModel, SeriesSearchResultModel
from MUComic.Qt.threads import PopulateThread, UpdateThread,DownloadThread,AddSeriesThread
import subprocess
import sys
import signal
from PySide import QtGui, QtCore


class UIStarter():
	def openIssue(self):
		issueindex = self.ui.listIssues.currentIndex()
		issue = self.ui.listIssues.model().data(issueindex,QtCore.Qt.UserRole)
		comicviewer = self.conn.config['MUComicLoad']['comicviewer']
		subprocess.Popen([comicviewer, self.conn.cbzfile(issue)])

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
		issueindex = self.ui.listIssues.currentIndex()
		issue = self.ui.listIssues.model().data(issueindex,QtCore.Qt.UserRole)
		#issue.downloading = True
		#self.issueModel.setData(issueindex, issue)
		if hasattr(self,'downloadThread') and self.downloadThread.isRunning():
			self.downloadThread.append([issue])
		else:
			self.downloadThread = DownloadThread([issue],self.conn,self.mw)
			#self.downloadThread.started.connect(lambda:self.ui.actionDownload.setDisabled(True))
			self.downloadThread.statusChanged.connect(self.notify)
			#self.downloadThread.finished.connect(lambda:self.ui.actionDownload.setDisabled(False))
			#self.downloadThread.terminated.connect(lambda:self.ui.actionDownload.setDisabled(False))
			self.downloadThread.done.connect(lambda:
					self.ui.listIssues.update(issueindex))
			self.downloadThread.start()

	def favSeries(self, fav):
		seriesindex = self.ui.listComics.currentIndex()
		series = self.ui.listComics.model().data(seriesindex,QtCore.Qt.UserRole)
		self.conn.db.set_series_faved(series.id, fav)
		series.fav = fav
		self.seriesmodel.setData(seriesindex, series)

	def addSeries(self):
		index = self.searchWindow.resultView.currentIndex()
		if index.row() != -1:
			if hasattr(self, "addSeriesThread") and self.addSeriesThread.isRunning():
				self.addSeriesThread.wait()
			else:
				series = self.searchWindow.resultView.model().data(index,QtCore.Qt.UserRole)
				self.addSeriesThread = AddSeriesThread(series.id,
						self.seriesmodel, self.conn)
				self.addSeriesThread.started.connect(lambda:self.ui.actionAdd_series.setDisabled(True))
				self.addSeriesThread.finished.connect(lambda:self.ui.actionAdd_series.setDisabled(False))
				self.addSeriesThread.terminated.connect(lambda:self.ui.actionAdd_series.setDisabled(False))
				self.addSeriesThread.finished.connect(self.updateSeriesModel)
				self.addSeriesThread.terminated.connect(self.updateSeriesModel)
				self.addSeriesThread.start()
		self.searchWindowForm.close()
	
	def updateSeriesModel(self):
		added_series = self.conn.get_added_series()
		self.seriesmodel.setDatas(added_series)

	def populateIssueModel(self, series):
		# If we have an old populate Thread, kill it
		if hasattr(self,'populateThread') and self.populateThread.isRunning():
			self.populateThread.abort()
			self.populateThread.wait()

		self.issueModel = IssueModel(self.conn, self.ui.listIssues)
		self.ui.listIssues.setModel(self.issueModel)
		self.populateThread = PopulateThread(self.issueModel, series, self.conn)
		self.populateThread.start()
		
	def updateIssuesModel(self, item):
		series = item.data(QtCore.Qt.UserRole)
		self.ui.actionFav_series.setChecked(series.fav)
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

	def setListView(self, listView):
		self.listView = listView 
		if listView:
			self.conn.config.set("UI", "FolderView", "False")
			self.ui.listIssues.setViewMode(QtGui.QListView.ListMode)
			self.ui.listIssues.setWrapping(True)
			self.ui.listIssues.setIconSize(QtCore.QSize(32,32))
		else:
			self.conn.config.set("UI", "FolderView", "True")
			self.ui.listIssues.setViewMode(QtGui.QListView.IconMode)
			self.ui.listIssues.setIconSize(QtCore.QSize(128,128))
		self.conn.updateConfig()
	
	def browseComicViewerClicked(self):
		comicViewer, snd = QtGui.QFileDialog.getOpenFileName()
		if comicViewer:
			self.settingswindow.le_comicViewer.setText(comicViewer)

	def browseDownloadDirClicked(self):
		downloadDir = QtGui.QFileDialog.getExistingDirectory()
		if downloadDir:
			self.settingswindow.le_download.setText(downloadDir)

	def searchButtonClicked(self):
		term = self.searchWindow.le_search.text()
		result = self.conn.db.search_series(term)
		self.searchmodel = SeriesModel(result,
				self.conn, self.searchWindow.resultView)
		self.searchWindow.resultView.setModel(self.searchmodel)

	def sigInt_handler(self, signal, frame):
		print("CTRL-C")

	def __init__(self, conn):
		self.conn = conn
		self.app = QtGui.QApplication(sys.argv)
		self.mw = QtGui.QMainWindow()
		self.ui = UI.Ui_MainWindow()
		self.ui.setupUi(self.mw)

		self.ui.actionFolder_View.setCheckable(True)
		self.ui.actionList_View.setCheckable(True)
		self.viewGroup = QtGui.QActionGroup(self.ui.menubar)
		self.viewGroup.addAction(self.ui.actionList_View)
		self.viewGroup.addAction(self.ui.actionFolder_View)
		if self.conn.config["UI"]["FolderView"] == "True":
			self.ui.actionFolder_View.setChecked(True)
		else:
			self.ui.actionList_View.setChecked(True)
			self.setListView(True)

		self.ui.listIssues.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
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

		self.searchWindow = SearchWindow.Ui_Form()
		self.searchWindowForm = QtGui.QDialog(self.mw)
		self.searchWindow.setupUi(self.searchWindowForm)
		self.searchWindow.bt_search.clicked.connect(self.searchButtonClicked)
		self.searchmodel = SeriesModel([], self.conn,
				self.searchWindow.resultView) 
		self.searchWindow.resultView.setModel(self.searchmodel)
		self.searchWindow.buttonBox.accepted.connect(self.addSeries)
		self.searchWindow.buttonBox.rejected.connect(self.searchWindowForm.close)

		self.ui.actionDownload.triggered.connect(self.downloadIssue)
		self.ui.menuFileSettings.triggered.connect(self.settingswindowform.show)
		self.ui.actionUpdate.triggered.connect(self.updateSeries)
		self.ui.actionAdd_series.triggered.connect(self.searchWindowForm.show)
		self.ui.actionFav_series.toggled.connect(self.favSeries)
		self.ui.actionOpen.triggered.connect(self.openIssue)
		self.ui.actionList_View.triggered.connect(lambda: self.setListView(True))
		self.ui.actionFolder_View.triggered.connect(lambda:
				self.setListView(False))
	
	def start(self):
		self.seriesmodel = SeriesModel(self.conn.get_added_series(), self.conn, self.ui.listComics)

		self.ui.listComics.setModel(self.seriesmodel)
		self.ui.listComics.clicked.connect(self.updateIssuesModel)

		self.issueModel = IssueModel(self.conn, self.ui.listIssues)
		if self.seriesmodel.rowCount(None) > 0:
			firstIndex = self.seriesmodel.index(0,0)
			firstseries = self.seriesmodel.data(firstIndex,QtCore.Qt.UserRole)
			self.populateIssueModel(firstseries)

		signal.signal(signal.SIGINT, signal.SIG_DFL)
		self.mw.show()
		sys.exit(self.app.exec_())
