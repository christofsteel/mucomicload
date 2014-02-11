from PySide import QtCore

class downloading(QtCore.QObject):
	sig = QtCore.Signal(int)

class downloadFinished(QtCore.QObject):
	sig = QtCore.Signal()

class SignalOnAppend(QtCore.QObject):
	sig = QtCore.Signal()

class UpdateFavedSeriesThread(QtCore.QThread):
	def __init__(self, model, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.model = model
		self.conn = model.conn

	def run(self):
		series = self.conn.get_faved_series()
		for s in series:
			self.conn.updateIssues(s)
			i = self.model.indexFor(s)
			self.model.setData(i, s)

class DownloadThread(QtCore.QThread):
	def __init__(self, issue, conn,parent=None):
		QtCore.QThread.__init__(self, parent)
		self.issue = issue
		self.conn = conn

	def run(self):
		self.conn.downloadIssue(self.issue)

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
						print("Downloading Cover for %s #%s" % (issue.title,
							issue.issue_number))
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
