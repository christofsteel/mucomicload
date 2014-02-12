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
		series = self.conn.get_faved_series()
		for s in series:
			self.conn.updateIssues(s)
			i = self.model.indexFor(s)
			self.model.setData(i, s)
		self.statusChanged.emit('Done')

class DownloadThread(QtCore.QThread):
	statusChanged = QtCore.Signal(str)
	def __init__(self, issue, conn,parent=None):
		QtCore.QThread.__init__(self, parent)
		self.issue = issue
		self.conn = conn

	def run(self):
		self.statusChanged.emit('Downloading %s #%s' % (self.issue.title,
			self.issue.safe_nr))
		self.conn.downloadIssue(self.issue)
		self.statusChanged.emit('Done')

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
	def __init__(self, theseries, model, conn, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.theseries = theseries
		self.model = model

	def run(self):
		pass
