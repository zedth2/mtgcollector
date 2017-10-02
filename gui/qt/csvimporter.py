#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

from PyQt5 import QtCore, QtGui, QtWidgets

class CSVImporter(QtWidgets.QWidget):
    def __init__(self, parent=None, windowflags=0, paths=[]):
        super().__init__(parent, QtCore.Qt.WindowFlags(windowflags))
        self.mainvly = QtWidgets.QHBoxLayout(self)
        self.btnTmp = QtWidgets.QPushButton('Import CSV')
        self.txtCollection = QtWidgets.QComboBox()
        self.txtCollection.setEditable(True)
        self.txtCollection.addItems(paths)
        self.mainvly.addWidget(self.txtCollection)
        self.mainvly.addWidget(self.btnTmp)

    def get_path(self):
        return self.txtCollection.currentText()
