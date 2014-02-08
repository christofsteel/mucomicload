from PySide import QtCore

class downloading(QtCore.QObject):
	sig = QtCore.Signal(int)

class downloadFinished(QtCore.QObject):
	sig = QtCore.Signal()

class SignalOnAppend(QtCore.QObject):
	sig = QtCore.Signal()

class DownloadThread(QtCore.QThread):
	def __init__(self, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.downloadingSignal = downloading()
		self.finishedDownloading = downloadFinished()

	def run(self):
		for i in range(101):
			self.msleep(100)
			self.downloadingSignal.sig.emit(i)
		self.finishedDownloading.sig.emit()

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
		for issue in self.series.issues:
			if not self._abort:
				self.model.append(issue)
		if not self._abort:
			for issue in self.series.issues:
				if not self._abort:
					if issue.cover == None:
						print("No Cover for Issue %s" % issue.issue_number)
						issue.cover = self.conn.getCover(issue)
						i = self.model.indexFor(issue)
						self.model.setData(i, issue)
