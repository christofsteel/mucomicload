# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/Search.ui'
#
# Created: Mon Feb 17 02:11:46 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.resize(471, 304)
		self.verticalLayout = QtGui.QVBoxLayout(Form)
		self.verticalLayout.setObjectName("verticalLayout")
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.le_search = QtGui.QLineEdit(Form)
		self.le_search.setObjectName("le_search")
		self.horizontalLayout.addWidget(self.le_search)
		self.bt_search = QtGui.QPushButton(Form)
		self.bt_search.setObjectName("bt_search")
		self.horizontalLayout.addWidget(self.bt_search)
		self.verticalLayout.addLayout(self.horizontalLayout)
		self.resultView = QtGui.QListView(Form)
		self.resultView.setObjectName("resultView")
		self.verticalLayout.addWidget(self.resultView)
		self.buttonBox = QtGui.QDialogButtonBox(Form)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setObjectName("buttonBox")
		self.verticalLayout.addWidget(self.buttonBox)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
		self.bt_search.setText(QtGui.QApplication.translate("Form", "Search", None, QtGui.QApplication.UnicodeUTF8))

