from PySide import QtCore

class downloading(QtCore.QObject):
	sig = QtCore.Signal(int)

class downloadFinished(QtCore.QObject):
	sig = QtCore.Signal()

class SignalOnAppend(QtCore.QObject):
	sig = QtCore.Signal()

class UpdateThread(QtCore.QThread):
	statusChanged = QtCore.Signal(str)
	def __init__(self, model, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.model = model
		self.conn = model.conn

	def run(self):
		self.statusChanged.emit('Downloading new series')
		self.conn.updateSeries()
		self.statusChanged.emit('Downloading new issue data')
		series = self.conn.get_added_series()
		for s in series:
			self.conn.updateIssues(s)
			i = self.model.indexFor(s)
			self.model.setData(i, s)
		self.statusChanged.emit("Downloading issues for faved series")
		fseries = self.conn.db.get_faved_series()
		for s in fseries:
			issues = self.conn.getIssues(s)
			for issue in issues:
				if not self.conn.issueHasLocal(issue) and not self.conn.issueHasTemp(issue):
					self.statusChanged.emit("Downloading issues for faved series (%s #%s)" % (issue.title, issue.safe_nr))
					self.conn.downloadIssue(issue)
		self.statusChanged.emit('Done')

class DownloadThread(QtCore.QThread):
	statusChanged = QtCore.Signal(str)
	done = QtCore.Signal()
	def __init__(self, issues, conn,parent=None):
		QtCore.QThread.__init__(self, parent)
		self.issues = issues
		self.conn = conn
		self.mutex = QtCore.QMutex()
		self.addIssues = []

	def append(self, issues):
		self.mutex.lock()
		self.addIssues += issues
		self.mutex.unlock()
	
	def downloadLoop(self):
		for issue in self.issues:
			self.statusChanged.emit('Downloading %s #%s' % (issue.title,
				issue.safe_nr))
			self.conn.downloadIssue(issue)
			self.statusChanged.emit('Done')
		self.mutex.lock()
		self.issues = self.addIssues
		self.addIssues = []
		self.mutex.unlock()
		if self.issues == []:
			self.done.emit()
			return
		else:
			self.downloadLoop()


	def run(self):
		self.downloadLoop()

class PopulateThread(QtCore.QThread):
	def __init__(self, model, series, conn, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.model = model
		self.series = series
		self.conn = conn
		self._abort = False

	def abort(self):
		self._abort = True

	def run(self):
		"""
			First populate the List, and then set the thumbnails. If no
			thumbnail exists, try downloading.
		"""
		for issue in self.conn.getIssues(self.series):
			if not self._abort:
				self.model.append(issue)
		if not self._abort:
			for issue in self.conn.getIssues(self.series):
				if not self._abort:
					if not issue.hasCover():
						issue.getCover()
						i = self.model.indexFor(issue)
						self.model.setData(i, issue)

class AddSeriesThread(QtCore.QThread):
	statusChanged = QtCore.Signal()
	def __init__(self, series_id, model, conn, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.series_id = series_id
		self.model = model
		self.conn = conn

	def run(self):
		self.conn.db.set_series_added(self.series_id, 1)
		series = self.conn.db.get_series(self.series_id)
		self.conn.updateIssues(series)
