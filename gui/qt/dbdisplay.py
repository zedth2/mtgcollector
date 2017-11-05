#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
import pprint
from PyQt5 import QtCore, QtGui, QtWidgets
from inventories import mtgdbhandler, sqlitehandler
from inventories import sqlments
from inventories import Collection, Deck, Set, Card

class CollectionItem(QtGui.QStandardItem):
    def __init__(self, collection=None, *args):
        super().__init__(*args)
        self.collection = collection
        self.setEditable(False)

class TableModel(QtGui.QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.rootItem = TreeItem(("ID", "Name", "Mana Cost"))
        self.setHorizontalHeaderItem(0, CollectionItem(None, "Name"))
        #self.setHorizontalHeaderItem(1, QtGui.QStandardItem("ID"))
        #self.setHorizontalHeaderItem(2, QtGui.QStandardItem("Mana Cost"))
        self.addrootitems()

    def add_sets(self, sets):
        magic = self.item_from_text('Magic')
        for s in sets:
            magic.appendRow(CollectionItem(s, s.name))

    def add_grouped_sets(self, sets):
        magic = self.item_from_text('Magic')
        for t, a in sets.items():
            stype = CollectionItem(None, t)
            a.sort(key=lambda a: a.name.lower())
            for s in a:
                stype.appendRow(CollectionItem(s, s.name))
            magic.appendRow(stype)

    def addtables(self, tables, parent=None):
        self.clear()
        c = 0

        #if parent is None:
            #parent = self.appendRow
        #elif isinstance(parent, QtGui.QStandardItem):
            #parent =
        while c < len(tables):
            name = CollectionItem(None, tables[c])
            name.setEditable(False)
            self.appendRow([name])
            c += 1
        #self.appendColumn(i)
        #self.appendColumn(i[1])

    def allrootitems(self):
        reLst = []
        cnt = 0
        while self.rowCount() > cnt:
            reLst.append(self.item(cnt, 0))
            cnt += 1
        return reLst

    def add_csv_tmp_collection(self, name):
        return self.add_collections([Collection(name, 'tmp/csv/', type='CSV_TEMP')])

    def add_tmp_collection(self, name):
        return self.add_collections([Collection(name, 'tmp/', type='TEMP')])

    def item_from_text(self, text):
        cnt = 0
        re = None
        while self.rowCount() > cnt:
            item = self.item(cnt, 0)
            if item.text() == text:
                re = item
                break
            cnt += 1
        return re

    def addrootitems(self):
        #i = [CollectionItem(None, 'Collections'), CollectionItem(None, 'Decks'), CollectionItem(None, 'Qube'), CollectionItem(None, 'Sets')]
        i = [CollectionItem(None, 'Magic')]
        c = 0
        while c < len(i):
            self.appendRow([i[c]])
            i[c].setEditable(False)
            c += 1
        return None

    def add_path(self, path, collection=None):
        s = path.split('/')
        items = self.findItems(s[0])
        item = None
        if 0 < len(items) and items[0].parent() is None:
            item = items[0]
        else:
            item = CollectionItem(collection, s[0])
            item.setEditable(False)
            self.appendRow(item)
        if len(s) < 2:
            return item
        for p in s[1:]:
            if p == '':
                continue
            i = self.check_children(item, p)
            if i is None:
                i = CollectionItem(collection, p)
                i.setEditable(False)
                item.appendRow(i)
            item = i
        return item

    def add_collections(self, items, select=True):
        item = None
        for i in items:
            item = self.add_path(i.path)
            c = CollectionItem(i, i.name)
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

    def get_cards(self, modelindex, store):
        cards = []
        item = self.itemFromIndex(modelindex)
        if item.collection is None: return cards
        #if isinstance(item.collection, Deck):
            #return store.get_cards_from_collection(item.collection)
        if isinstance(item.collection, Set):
            return store.get_all_cards_from_set(item.collection)
        elif isinstance(item.collection, Collection):
            item.collection.cards = store.get_cards_from_collection(item.collection)
            return item.collection.cards

class DatabaseDisplay(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = mtgdbhandler.MTGDatabaseHandler()
        self.model = TableModel(self)
        self.setModel(self.model)
        #self.model.addrootitems()

    def new_database(self, dbfile):
        self.store = mtgdbhandler.MTGDatabaseHandler(dbfile)
        self.store.create_new_db(dbfile)

    def click(self, *args):
        pass

    def open_database(self, dbfile):
        self.store.open_file(dbfile)
        #self.model.addtables(self.store.gettables())
        self.model.add_collections(self.store.get_all_userbuilds())
        #self.model.add_sets(self.store.all_sets())
        self.model.add_grouped_sets(self.store.get_all_sets_by_type())

    def add_collection(self, path, name, skipdb=False, select=True):
        if not skipdb and not len(self.store.get_collection(path, name)):
            self.store.create_new_collection(path, name)
        #item = self.model.add_collections(self.store.get_all_userbuilds())
        if select and item is not None:
            self.scrollTo(item.index())
            self.selectionModel().select(item.index(), QtCore.QItemSelectionModel.Select)

    def loadtable(self, tablename):
        self.gal.model.addtables(self.store.get_table_items(tablename))

    def listtables(self):
        self.add_collection('database/', sqlments.MTGCARDS_TABLE_NAME)

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

    def selected_collections(self):
        cols = []
        for mi in self.selectedIndexes():
            cols.append(self.model.itemFromIndex(mi).collection)
        return cols

if __name__ == '__main__':
    pass
