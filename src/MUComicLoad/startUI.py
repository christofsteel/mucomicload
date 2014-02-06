import UI
import sys
import Database
from PySide import QtGui, QtCore

class SeriesModel(QtCore.QAbstractListModel):
	def __init__(self, series, parent=None):
		QtCore.QAbstractListModel.__init__(self, parent)
		self._series = series

	def rowCount(self,role):
		return len(self._series)

	def data(self, index, role):
		if role == QtCore.Qt.DisplayRole:
			return self._series[index.row()][1]
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
		if role == QtCore.Qt.DisplayRole:
			return "%s #%s" % (self._issues[index.row()][3],
					safe_nr(self._issues[index.row()][0]))
		else:
			return None


def safe_nr(nr):
	if type(nr) is int:
		return '%03d' % nr
	elif type(nr) is str:
		if '.' in nr:
			split = [int(i) for i in nr.split('.')]
			split[0] = "%03d" % split[0]
			return ".".join([str(s) for s in split])
		else:
			return safe_nr(int(nr))
	else:
		print("Unrecognized issue number")
		return str(nr)

def updateIssues(item):
	series_id = item.data(QtCore.Qt.UserRole)[0]
	newModel = IssueModel(db.get_issue_list(series_id), ui.listIssues)
	ui.listIssues.setModel(newModel)



db = Database.DB("/home/christoph/.mucomics.db")

app = QtGui.QApplication(sys.argv)
mw = QtGui.QMainWindow()
ui = UI.Ui_MainWindow()
ui.setupUi(mw)

seriesmodel = SeriesModel(db.get_faved_series(), ui.listComics)

firstIndex = seriesmodel.index(0,0)

#issuemodel = IssueModel(db.get_issue_list(seriesmodel.data(firstIndex, QtCore.Qt.UserRole)), ui.listIssues)
"""
for item in db.get_faved_series():
	qitem = QtGui.QStandardItem(item[1])
	qitem.setData(item[0])
	seriesmodel.appendRow(qitem)
"""
ui.listComics.setModel(seriesmodel)
ui.listComics.clicked.connect(updateIssues)
#ui.listIssues.setModel(issuemodel)

mw.show()
app.exec_()
