#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from mtgsdk import Card

from utils.mana import manaconversion, downloadimg

from utils.config import DEFAULT_CARD_ICON


class CardItem(QtGui.QStandardItem):
    def __init__(self, card, *args):
        self.card = card
        self.iconpath = DEFAULT_CARD_ICON
        if len(args):
            super().__init__(*args)
        else:
            if self.iconpath is None:
                super().__init__(card.name)
            else:

                super().__init__(QtGui.QIcon(self.iconpath), card.name)
        self.setEditable(False)

    def getimage(self):
        self.iconpath = downloadimg(self.card)
        self.setIcon(QtGui.QIcon(self.iconpath))

class CardModel(QtGui.QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.rootItem = TreeItem(("ID", "Name", "Mana Cost"))

    def addcards(self, cards):
        self.clear()
        c = 0
        while c < len(cards):
            card = CardItem(cards[c])
            card.getimage()
            self.appendRow(card)
            c += 1

    def threadcardadds(self, cards):
        threading.Thread(target=self.addcards, args=(cards,)).start()

class CardTableModel(CardModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_header()

    def set_header(self):
        self.setHorizontalHeaderItem(0, QtGui.QStandardItem("Name"))
        self.setHorizontalHeaderItem(1, QtGui.QStandardItem("ID"))
        self.setHorizontalHeaderItem(2, QtGui.QStandardItem("Mana Cost"))

    def threadcardadds(self, cards):
        threading.Thread(target=self.addtreecards, args=(cards,)).start()

    def addtreecards(self, cards):
        self.clear()
        self.set_header()
        c = 0
        while c < len(cards):
            card = cards[c]
            child = CardItem(card, card.id)
            name = CardItem(card, card.name)
            mana = CardItem(card, card.mana_cost)
            self.appendRow([name, child, mana])
            c += 1

class CardTable(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = CardTableModel(self)
        self.setModel(self.model)

class CardGallery(QtWidgets.QListView):
    def __init__(self, parent=None, model=None):
        super().__init__(parent)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setIconSize(QtCore.QSize(223, 310))
        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setUniformItemSizes(True)
        self.setWordWrap(True)
        self.setupmodel(model)

    def setupmodel(self, model=None):
        if model is None:
            model = CardModel(self)

        self.model = CardModel(self)
        self.setModel(self.model)

    def selected_cards(self, count=1):
        cols = []
        for mi in self.selectedIndexes():
            card = self.model.itemFromIndex(mi).card
            print('SELECTED CARD ', card.name, ' COUNT ', card.count)
            card.count = count
            cols.append(card)
        return cols

    def item(self, row, col=0):
        return self.model.item(row, col)

class CardTree(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = CardModel(self)
        self.setModel(self.model)
