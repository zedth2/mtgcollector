#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
import logging
from os import environ
from os.path import basename

from PyQt5 import QtCore, QtGui, QtWidgets

from .cardgallery import CardGallery, CardTable
from .cardetails import CardDetails
from .dbdisplay import DatabaseDisplay
from .csvimporter import CSVImporter
from inventories import sqlitehandler
from inventories import Collection, Deck, Set, Card

class ActionCollection(QtWidgets.QAction):
    def __init__(self, collection, callback, *args):
        super().__init__(*args)
        self.collection = collection
        self.setText(self.collection.path + '/' + self.collection.name)
        self.callback = callback
        self.triggered.connect(self.clicked)

    def clicked(self):
        self.callback(self.collection)

class MTGCollections(QtWidgets.QWidget):
    def __init__(self, parent=None, windowflags=0):
        super().__init__(parent, QtCore.Qt.WindowFlags(windowflags))
        self.resize(782, 570)
        self.mainh = QtWidgets.QHBoxLayout(self)
        self.mainhlyo = QtWidgets.QSplitter(self)
        self.mainh.addWidget(self.mainhlyo)

        self.databaseinfo = DatabaseDisplay(self)
        self.databaseinfo.clicked.connect(self.click)
        self.mainhlyo.addWidget(self.databaseinfo)

        #self.csvimp = CSVImporter(self)
        self.csvimp = CardTable(self)
        #self.csvimp.btnTmp.clicked.connect(self.clickimport)
        self.gal = CardGallery(self)
        self.gal.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.gal.customContextMenuRequested.connect(self.rightclick)

        self.galcsvholder = QtWidgets.QWidget(self)
        self.galvly = QtWidgets.QVBoxLayout(self)
        self.galvly.addWidget(self.gal)
        self.galvly.addWidget(self.csvimp)
        self.galcsvholder.setLayout(self.galvly)
        self.mainhlyo.addWidget(self.galcsvholder)
        #self.gal.model.threadcardadds(self.getStuff())
        #self.mainhlyo.addWidget(self.gal)
        self.gal.clicked['QModelIndex'].connect(self.clicked)
        self.det = CardDetails(self)
        self.mainhlyo.addWidget(self.det)

        self.create_menu()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.tmps = {}

    def create_menu(self):
        self.mnsMain = QtWidgets.QMenuBar(self)
        self.mnsFile = QtWidgets.QMenu(self.mnsMain)
        self.mnsFile.setTitle('&File')

        self.mnsNew = QtWidgets.QAction(self)
        self.mnsNew.setText('&New')
        self.mnsNew.triggered.connect(self.new)
        self.mnsFile.addAction(self.mnsNew)

        self.mnsOpen = QtWidgets.QAction(self)
        self.mnsOpen.setText('&Open')
        self.mnsOpen.triggered.connect(self.open)
        self.mnsFile.addAction(self.mnsOpen)

        self.mnsSave = QtWidgets.QAction(self)
        self.mnsSave.setText('&Save')
        self.mnsSave.triggered.connect(self.save)
        self.mnsFile.addAction(self.mnsSave)

        self.mnsImport = QtWidgets.QAction(self)
        self.mnsImport.setText('&Import')
        self.mnsImport.triggered.connect(self.importcsv)
        self.mnsFile.addAction(self.mnsImport)

        self.mnsExport = QtWidgets.QAction(self)
        self.mnsExport.setText('&Export')
        self.mnsExport.triggered.connect(self.exportcsv)
        self.mnsFile.addAction(self.mnsExport)
        self.layout().setMenuBar(self.mnsMain)
        self.mnsMain.addAction(self.mnsFile.menuAction())
        self.create_context()

    def create_context(self):
        self.mnsCollections = QtWidgets.QMenu(self.mnsMain)
        self.mnsCollections.setTitle('&Collection')

        self.mnsNewColl = QtWidgets.QAction(self)
        self.mnsNewColl.setText('&New Collection')
        self.mnsNewColl.triggered.connect(self.newcollection)
        self.mnsCollections.addAction(self.mnsNewColl)


        self.mnsNewColl = QtWidgets.QAction(self)
        self.mnsNewColl.setText('&Paths')
        self.mnsNewColl.triggered.connect(self.addpaths)
        self.mnsCollections.addAction(self.mnsNewColl)
        self.mnsMain.addAction(self.mnsCollections.menuAction())

    def create_right_context(self):
        if self.databaseinfo.store is None:
            return QtWidgets.QMenu()
        self.mnsContext = QtWidgets.QMenu()
        mnsAddCollections = QtWidgets.QMenu('Collections', self.mnsContext)
        for c in self.databaseinfo.store.get_all_userbuilds():
            act = ActionCollection(c, self.add_collection, self.mnsContext)
            mnsAddCollections.addAction(act)
        self.mnsContext.addMenu(mnsAddCollections)
        return self.mnsContext

    def add_collection(self, collection):
        cards = self.gal.selected_cards()
        if len(cards):
            self.databaseinfo.store.add_cards_userbuild(collection, cards)

    def addpaths(self):
        items = self.databaseinfo.model.get_all_paths()
        adds = []
        for i in items:
            if not i.startswith('tmp/') or i != 'tmp':
                adds.append(i)
        self.csvimp.txtCollection.addItems(adds)

    def rightclick(self, *args):
        cols = self.databaseinfo.selected_collections()
        for c in cols:
            if isinstance(c, Set):
                print('SELECTED A SET')
        self.create_right_context().popup(self.gal.mapToGlobal(args[0]))
        print('FUCK', *args)

    def clicked(self, *args):
        #print("CLICKED", args)
        self.det.change_card(self.gal.item(args[0].row(), args[0].column()).card)
        #print(self.listView.item(args[0].row(), args[0].column()).card)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))

    def getStuff(self):
        return self.databaseinfo.store.csvr()

    def opendatabase(self, dbfile):
        self.databaseinfo.open_database(dbfile)

    def clickimport(self):
        path = self.databaseinfo.selected_path()
        base = path.rsplit('/',1)[-1]
        if not path.startswith('tmp/'):
            return

        self.databaseinfo.store.insertcards(self.tmps[base])
        wpath = self.csvimp.get_path().rsplit('/', 1)
        path = wpath[0]
        name = wpath[1]
        wpath = self.databaseinfo.selected_path().rsplit('/', 1)
        selected_path = wpath[0]
        selected_name = wpath[1]
        self.databaseinfo.store.insert_into_collection(path, name, self.tmps[selected_name])

    def click(self, modelindex):
        if self.databaseinfo.store is None:
            return
        item = self.databaseinfo.model.itemFromIndex(modelindex)
        if item.collection is None: return
        try:
            if self.loadtmp(item.collection.path): return
        except AttributeError: #If it's not a class of type Collection
            pass
        try:
            cards = self.databaseinfo.model.get_cards(modelindex, self.databaseinfo.store)
            logging.debug('Attempting to load ' + str(type(item.collection)) + ' ' + str(item.collection.name) + ' total cards found ' + str(len(cards)))
            self.gal.model.threadcardadds(cards)
            self.csvimp.model.threadcardadds(cards)
        except Exception as ex:
            print('EXCEPTION ', ex)

    def loadtmp(self, path):
        if path.startswith('tmp/'):
            if path.split('/')[-1] in self.tmps:
                self.gal.model.threadcardadds(self.tmps[path.split('/')[-1]])
                return True
        return False

    def open(self, *args):
        f = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Database', environ['HOME']+'/Documents/Code/PythonFunctions/projects/mtg/inventories')
        if '' == f[0]:
            return
        self.databaseinfo.open_database(f[0])

    def save(self, *args):
        pass

    def importcsv(self, *args):
        f = QtWidgets.QFileDialog.getOpenFileName(self, 'Import CSV', environ['HOME']+'/Documents/Code/PythonFunctions/projects/mtg/inventories')
        if '' == f[0]:
            return
        base = basename(f[0])
        if base in self.tmps: #If it's already being shown we should also select it
            return
        self.databaseinfo.add_collection('tmp/', base, True)
        self.addpaths()
        self.tmps[base] = self.databaseinfo.store.csvr(f[0])

    def exportcsv(self, *args):
        pass

    def new(self):
        f = QtWidgets.QFileDialog.getSaveFileName(self, 'New Database', environ['HOME']+'/Documents/Code/PythonFunctions/projects/mtg')
        if '' == f[0]:
            return
        try:
            self.databaseinfo.store.openDB.close()
        except AttributeError:
            pass #Probably no loaded file...you know probably
        self.databaseinfo.store.create_new_db(f[0])
        self.databaseinfo.open_database(f[0])

    def newcollection(self):
        collection = QtWidgets.QInputDialog.getText(self, 'New Collection', 'Collection Path/Name')
        if not collection[1]: return
        c = collection[0].rsplit('/', 1)
        path = c[0]
        name = c[1]
        self.databaseinfo.add_collection(path, name)
