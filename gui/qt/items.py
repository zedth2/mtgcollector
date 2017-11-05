#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
from PyQt5 import QtGui

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


class SetItem(QtGui.QStandardItem):
    def __init__(self, set, *args):
        self.set = set
        self.iconpath = None
        if len(args):
            super().__init__(*args)
        else:
            if self.iconpath is None:
                super().__init__(self.set.name)
            else:
                super().__init__(QtGui.QIcon(self.iconpath), self.set.name)
        self.setEditable(False)
