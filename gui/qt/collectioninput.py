#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

from PyQt5 import QtCore, QtGui, QtWidgets


class CollectionInput(QtWidgets.QWidget):
    def __init__(self, parent=None, windowflags=0):
        super().__init__(parent, QtCore.Qt.WindowFlags(windowflags))
