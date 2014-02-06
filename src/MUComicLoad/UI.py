# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created: Wed Feb  5 20:04:06 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.horizontalSplit = QtGui.QWidget(MainWindow)
        self.horizontalSplit.setObjectName("horizontalSplit")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalSplit)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.listComics = QtGui.QListView(self.horizontalSplit)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listComics.sizePolicy().hasHeightForWidth())


        self.listComics.setSizePolicy(sizePolicy)
        self.listComics.setObjectName("listComics")

        self.horizontalLayout_3.addWidget(self.listComics)
        self.listIssues = QtGui.QListView(self.horizontalSplit)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listIssues.sizePolicy().hasHeightForWidth())
        self.listIssues.setSizePolicy(sizePolicy)
        self.listIssues.setObjectName("listIssues")
        self.listIssues.setViewMode(QtGui.QListView.IconMode)
        self.listIssues.setIconSize(QtCore.QSize(128,128))
        self.horizontalLayout_3.addWidget(self.listIssues)
        MainWindow.setCentralWidget(self.horizontalSplit)
        self.menubar = QtGui.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.menuFileSettings = QtGui.QAction(MainWindow)
        self.menuFileSettings.setObjectName("menuFileSettings")
        self.menuFileQuit = QtGui.QAction(MainWindow)
        self.menuFileQuit.setObjectName("menuFileQuit")
        self.actionAdd_series = QtGui.QAction(MainWindow)
        self.actionAdd_series.setObjectName("actionAdd_series")
        self.actionUpdate = QtGui.QAction(MainWindow)
        self.actionUpdate.setObjectName("actionUpdate")
        self.actionAbout_MUComicLoad = QtGui.QAction(MainWindow)
        self.actionAbout_MUComicLoad.setObjectName("actionAbout_MUComicLoad")
        self.actionHelp = QtGui.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.menuFile.addAction(self.actionUpdate)
        self.menuFile.addAction(self.actionAdd_series)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuFileSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuFileQuit)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_MUComicLoad)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionUpdate)
        self.toolBar.addAction(self.actionAdd_series)
        self.toolBar.addAction(self.menuFileSettings)
        self.toolBar.addAction(self.actionHelp)
        """
        self.actionAdd_series.setIcon(QtGui.QIcon.fromTheme('application-exit', self.horizontalSplit.style().standardIcon(QtGui.QStyle.SP_FileDialogNewFolder)))
        self.actionUpdate.setIcon(self.horizontalSplit.style().standardIcon(QtGui.QStyle.SP_BrowserReload))
        self.menuFileSettings.setIcon(self.horizontalSplit.style().standardIcon(QtGui.QStyle.SP_TitleBarContextHelpButton))
        self.actionHelp.setIcon(self.horizontalSplit.style().standardIcon(QtGui.QStyle.SP_DialogHelpButton))
        self.menuFileQuit.setIcon(self.horizontalSplit.style().standardIcon(QtGui.QStyle.SP_TitleBarCloseButton))
        """
        self.actionAdd_series.setIcon(QtGui.QIcon('res/addseries.png'))
        self.actionUpdate.setIcon(QtGui.QIcon('res/update.png'))
        self.menuFileSettings.setIcon(QtGui.QIcon('res/settings.png'))
        self.actionHelp.setIcon(QtGui.QIcon('res/help.png'))
        self.menuFileQuit.setIcon(QtGui.QIcon('res/exit.png'))


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFileSettings.setText(QtGui.QApplication.translate("MainWindow", "&Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFileQuit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_series.setText(QtGui.QApplication.translate("MainWindow", "&Add series", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUpdate.setText(QtGui.QApplication.translate("MainWindow", "&Update", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_MUComicLoad.setText(QtGui.QApplication.translate("MainWindow", "About MUComicLoad", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setText(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))

