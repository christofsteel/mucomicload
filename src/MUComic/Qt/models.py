from PySide import QtCore, QtGui


class SeriesModel(QtCore.QAbstractListModel):
	def __init__(self, series, conn, parent=None):
		QtCore.QAbstractListModel.__init__(self, parent)
		self._series = series
		self.conn = conn

	def rowCount(self,role):
		return len(self._series)

	def setDatas(self, series):
		self._series = series
		start = self.createIndex(0,0)
		end = self.createIndex(len(self._series)-1, 0)
		self.dataChanged.emit(start, end)

	def setData(self, index, value, role=QtCore.Qt.EditRole):
		if role != QtCore.Qt.EditRole:
			return False
		if index.isValid() and 0 <= index.row() < len(self._series):
			self._series[index.row()] = value
			self.dataChanged.emit(index, index)

	def indexFor(self, obj):
		return self.index(self._series.index(obj),0)

	def data(self, index, role):
		if role == QtCore.Qt.DisplayRole:
			return self._series[index.row()].title
		elif role == QtCore.Qt.DecorationRole:
			img = self.conn.getFirstCover(self._series[index.row()])
			if img:
				qimg = QtGui.QImage.fromData(img, 'JPG')
			else:
				img = open('res/missing.png', 'rb').read()
				qimg = QtGui.QImage.fromData(img, 'png')
			qpix = QtGui.QPixmap.fromImage(qimg)
			return QtGui.QIcon(qpix)
		elif role == QtCore.Qt.UserRole:
			return self._series[index.row()]
		else:
			return None

class IssueModel(QtCore.QAbstractListModel):
	def __init__(self, parent=None):
		QtCore.QAbstractListModel.__init__(self, parent)
		self._issues = []

	def append(self, issue):
		self.beginInsertRows(QtCore.QModelIndex(), len(self._issues)-1,
				len(self._issues))
		self._issues.append(issue)
		index = self.index(len(self._issues)-1, 0)
		self.endInsertRows()
		self.dataChanged.emit(index, index)

	def setData(self, index, value, role=QtCore.Qt.UserRole):
		if role != QtCore.Qt.UserRole:
			return False
		if index.isValid() and 0 <= index.row() < len(self._issues):
			self._issues[index.row()] = value
			self.dataChanged.emit(index, index)

	def indexFor(self, obj):
		return self.index(self._issues.index(obj),0)

	def rowCount(self, role):
		return len(self._issues)

	def data(self, index, role):
		issue = self._issues[index.row()]
		if role == QtCore.Qt.DisplayRole:
			return "#%s" % (issue.safe_nr)
		elif role == QtCore.Qt.DecorationRole:
			if issue.hasCover():
				qimg = QtGui.QImage.fromData(issue.cover(), 'JPG')
			else:
				img = open('res/missing.png', 'rb').read()
				qimg = QtGui.QImage.fromData(img, 'png')
			if issue.local():
				okpix = QtGui.QPixmap('res/ok.png')
			else:
				okpix = QtGui.QPixmap('res/notok.png')
			qpix = QtGui.QPixmap.fromImage(qimg)
			qrect = qpix.rect()
			miniokpix = okpix.scaled(64,64)
			painter = QtGui.QPainter(qpix)
			painter.drawPixmap(qrect.width()-64,qrect.height()-64,miniokpix)
			painter.end()
			return QtGui.QIcon(qpix)
		elif role == QtCore.Qt.UserRole:
			return issue
		else:
			return None

