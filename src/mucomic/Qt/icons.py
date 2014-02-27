from PySide import QtGui

def addThemedIcon(action, name):
	icon = action.icon()
	nicon = QtGui.QIcon.fromTheme(name, icon)
	action.setIcon(nicon)

def changeIconsUI(ui):
	addThemedIcon(ui.menuFileSettings, 'preferences-system')
	addThemedIcon(ui.menuFileQuit, 'system-log-out')
	addThemedIcon(ui.actionAdd_series, 'list-add')
	addThemedIcon(ui.actionRemove_series, 'list-remove')
	addThemedIcon(ui.actionUpdate, 'view-refresh')
	addThemedIcon(ui.actionDownload_Issue, 'go-bottom')
	addThemedIcon(ui.actionDownload_Series, 'go-bottom')
	addThemedIcon(ui.actionDownload, 'go-bottom')
	addThemedIcon(ui.actionOpen, 'edit-find')
	addThemedIcon(ui.actionFav_series, 'emblem-favourite')
