#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
from sys import argv, exit
from PyQt5 import QtCore, QtGui, QtWidgets
from gui.qt import MTGCollections
from utils import logsetup

def main(*args):
    app = QtWidgets.QApplication(list(args))
    Form = MTGCollections()
    Form.show()
    #Form.opendatabase()
    exit(app.exec_())



if __name__ == '__main__':
    main(*argv)
