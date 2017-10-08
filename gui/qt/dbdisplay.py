#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
import pprint
from PyQt5 import QtCore, QtGui, QtWidgets
from inventories import sqlitehandler

class TableModel(QtGui.QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.rootItem = TreeItem(("ID", "Name", "Mana Cost"))
        self.setHorizontalHeaderItem(0, QtGui.QStandardItem("Name"))
        #self.setHorizontalHeaderItem(1, QtGui.QStandardItem("ID"))
        #self.setHorizontalHeaderItem(2, QtGui.QStandardItem("Mana Cost"))
        #self.addrootitems()

    def addtables(self, tables, parent=None):
        self.clear()
        c = 0

        #if parent is None:
            #parent = self.appendRow
        #elif isinstance(parent, QtGui.QStandardItem):
            #parent =
        while c < len(tables):
            name = QtGui.QStandardItem(tables[c])
            name.setEditable(False)
            self.appendRow([name])
            c += 1
        #self.appendColumn(i)
        #self.appendColumn(i[1])

    def addrootitems(self):
        i = [QtGui.QStandardItem('Collections'), QtGui.QStandardItem('Decks'), QtGui.QStandardItem('Qube'), QtGui.QStandardItem('Sets')]
        c = 0
        while c < len(i):
            self.appendRow([i[c]])
            i[c].setEditable(False)
            c += 1
        return None

    def add_path(self, path):
        s = path.split('/')
        items = self.findItems(s[0])
        item = None
        if 0 < len(items) and items[0].parent() is None:
            item = items[0]
        else:
            item = QtGui.QStandardItem(s[0])
            item.setEditable(False)
            self.appendRow(item)
        if len(s) < 2:
            return item
        for p in s[1:]:
            if p == '':
                continue
            i = self.check_children(item, p)
            if i is None:
                i = QtGui.QStandardItem(p)
                i.setEditable(False)
                item.appendRow(i)
            item = i
        return item

    def add_collections(self, items, select=True):
        item = None
        for i in items:
            item = self.add_path(i[1])
            c = QtGui.QStandardItem(i[2])
            c.setEditable(False)
            item.appendRow(c)
            item = c
        return item

    def check_children(self, parent, text):
        item = None
        if not parent.hasChildren():
            return None
        c = 0
        while c < parent.rowCount():
            ch = parent.child(c, 0)
            if ch is not None and text == ch.text():
                item = ch
                break
            c += 1
        return item

    def get_all_paths(self):
        item = None
        paths = []
        cnt = 0
        while cnt < self.rowCount():
            paths += self.get_path(self.item(cnt, 0))
            cnt += 1
        return paths

    def get_path(self, item):
        path = item.text()
        items = []
        paths = []
        cnt = 0
        while cnt < item.rowCount():
            items += self.get_path(item.child(cnt, 0))
            cnt += 1
        for i in items:
            paths.append(path+'/'+i)
        return [path] + paths

    def get_path_from_child(self, item):
        path = item.text()
        parent = item.parent()
        while parent is not None:
            path = parent.text() + '/' + path
            parent = parent.parent()
        return path


class DatabaseDisplay(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = sqlitehandler.Store()
        self.model = TableModel(self)
        self.setModel(self.model)
        self.model.addrootitems()

    def new_database(self, dbfile):
        self.store = sqlitehandler.Store(dbfile)
        self.store.create_new_db(dbfile)

    def click(self, *args):
        pass

    def open_database(self, dbfile):
        self.store.open_file(dbfile)
        #self.model.addtables(self.store.gettables())
        self.model.add_collections(self.store.get_collection_information())

    def add_collection(self, path, name, skipdb=False, select=True):
        if not skipdb and not self.store.collection_exists(path, name):
            self.store.create_new_collection(path, name)
        item = self.model.add_collections([(None, path, name, None)])
        if select and item is not None:
            self.scrollTo(item.index())
            self.selectionModel().select(item.index(), QtCore.QItemSelectionModel.Select)

    def loadtable(self, tablename):
        self.gal.model.addtables(self.store.get_table_items(tablename))

    def get_path(self, item):
        path = item.text()
        parent = item.parent()
        while parent is not None:
            path = parent.text() + '/' + path
            parent = parent.parent()
        return path

    def selected_path(self):
        path = ''
        for i in self.selectedIndexes():
            path = self.model.get_path_from_child(self.model.itemFromIndex(i))
        return path

if __name__ == '__main__':
    pass
