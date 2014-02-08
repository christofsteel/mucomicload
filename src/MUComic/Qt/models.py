from PySide import QtCore, QtGui


class SeriesModel(QtCore.QAbstractListModel):
	def __init__(self, series, parent=None):
		QtCore.QAbstractListModel.__init__(self, parent)
		self._series = series

	def rowCount(self,role):
		return len(self._series)

	def data(self, index, role):
		if role == QtCore.Qt.DisplayRole:
			return self._series[index.row()].title
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
			return "#%s" % (self.safe_nr(issue.issue_number))
		elif role == QtCore.Qt.DecorationRole:
			if issue.cover != None:
				qimg = QtGui.QImage.fromData(issue.cover, 'JPG')
			else:
				img = open('res/missing.png', 'rb').read()
				qimg = QtGui.QImage.fromData(img, 'png')
			if issue.local:
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
		else:
			return None

	def safe_nr(self,nr):
		if type(nr) is int:
			return '%03d' % nr
		elif type(nr) is str:
			if '.' in nr:
				split = [int(i) for i in nr.split('.')]
				split[0] = "%03d" % split[0]
				return ".".join([str(s) for s in split])
			else:
				return self.safe_nr(int(nr))
		else:
			print("Unrecognized issue number")
			return str(nr)