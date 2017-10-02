#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

from PyQt5 import QtCore, QtGui, QtWidgets
from mtgsdk import Card

from utils.mana import downloadimg

class CardDetails(QtWidgets.QWidget):
    def __init__(self, parent=None, flags=0):
        super().__init__(parent, QtCore.Qt.WindowFlags(flags))
        self.mainvly = QtWidgets.QVBoxLayout(self)
        self.lblCard = QtWidgets.QLabel(self)
        self.mainvly.addWidget(self.lblCard)
        self.txtInfo = QtWidgets.QTextEdit(self)
        self.docText = QtGui.QTextDocument(self)
        self.txtInfo.setDocument(self.docText)
        self.mainvly.addWidget(self.txtInfo)

        self.card = None

    def change_card(self, card):
        self.card = card
        img = downloadimg(self.card)
        self.lblCard.setPixmap(QtGui.QPixmap(img))
        #self.lblCard.setText(self.card.name)
        text = self.card.text if self.card.text else ''
        self.docText.setPlainText(text + '\n' + img)
