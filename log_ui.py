from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LogWindow(object):
    def setupUi(self, LogWindow):
        LogWindow.setObjectName("LogWindow")
        LogWindow.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(LogWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.status_label = QtWidgets.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(10, 10, 581, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.status_label.setFont(font)
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setObjectName("status_label")
        self.log_table = QtWidgets.QTableWidget(self.centralwidget)
        self.log_table.setGeometry(QtCore.QRect(10, 50, 581, 341))
        self.log_table.setObjectName("log_table")
        self.log_table.setColumnCount(2)
        self.log_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.log_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.log_table.setHorizontalHeaderItem(1, item)
        LogWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LogWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName("menubar")
        LogWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LogWindow)
        self.statusbar.setObjectName("statusbar")
        LogWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LogWindow)
        QtCore.QMetaObject.connectSlotsByName(LogWindow)

    def retranslateUi(self, LogWindow):
        _translate = QtCore.QCoreApplication.translate
        LogWindow.setWindowTitle(_translate("LogWindow", "Log Viewer"))
        self.status_label.setText(_translate("LogWindow", "Waiting for packets..."))
        item = self.log_table.horizontalHeaderItem(0)
        item.setText(_translate("LogWindow", "Date/Time"))
        item = self.log_table.horizontalHeaderItem(1)
        item.setText(_translate("LogWindow", "Attack Type"))
