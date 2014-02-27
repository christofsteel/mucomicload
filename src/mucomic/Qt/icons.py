from PySide import QtGui

def addThemedIcon(action, name):
	icon = action.icon()
	nicon = QtGui.QIcon.fromTheme(name, icon)
	action.setIcon(nicon)

def changeIconsUI(ui):
	addThemedIcon(ui.menuFileSettings, 'preferences-system')
