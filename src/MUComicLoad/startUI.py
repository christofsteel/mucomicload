import MUComicLoad.UI as UI
import sys
from PySide import QtGui, QtCore

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
	def __init__(self, issues, parent=None):
		QtCore.QAbstractListModel.__init__(self, parent)
		self._issues = issues

	def rowCount(self, role):
		return len(self._issues)

	def data(self, index, role):
		issue = self._issues[index.row()]
		if role == QtCore.Qt.DisplayRole:
			return "#%s" % (self.safe_nr(issue.issue_number))
		elif role == QtCore.Qt.DecorationRole:
			return QtGui.QIcon('res/test.jpg')
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

class UIStarter():
	def updateIssues(self, item):
		series_id = item.data(QtCore.Qt.UserRole)[0]	# Weird, item.data returns 
														# list instead of NamedTuple
		newModel = IssueModel(self.db.get_issue_list(series_id), self.ui.listIssues)
		self.ui.listIssues.setModel(newModel)

	def __init__(self, db, api):
		self.db = db
		app = QtGui.QApplication(sys.argv)
		mw = QtGui.QMainWindow()
		self.ui = UI.Ui_MainWindow()
		self.ui.setupUi(mw)

		seriesmodel = SeriesModel(db.get_faved_series(), self.ui.listComics)

		firstIndex = seriesmodel.index(0,0)
		firstseries_id = (seriesmodel.data(firstIndex,QtCore.Qt.UserRole)).id

		issuemodel = IssueModel(db.get_issue_list(firstseries_id), self.ui.listIssues)

		self.ui.listComics.setModel(seriesmodel)
		self.ui.listComics.clicked.connect(self.updateIssues)
		self.ui.listIssues.setModel(issuemodel)

		mw.show()
		app.exec_()
