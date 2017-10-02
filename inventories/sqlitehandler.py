#!/usr/bin/python3
'''
Author : Zachary Harvey






'''


import sqlite3 as sql
import json
import csv

from mtgsdk import Card, QueryBuilder
from mtgsdk.config import __endpoint__

from utils import CardItem
from utils.config import URL_LENGTH

MTG_CARDS_TABLE_NAME = 'mtgcards'
MTG_CARDS = '''CREATE TABLE '''+MTG_CARDS_TABLE_NAME + '''
                    (name TEXT, --Orginal Type <class 'str'>
                    layout TEXT, --Orginal Type <class 'str'>
                    mana_cost TEXT, --Orginal Type <class 'str'>
                    cmc INTEGER, --Orginal Type <class 'int'>
                    colors TEXT, --Orginal Type <class 'list'> This should be a comma seperated list of all the values
                    -- color_identity TEXT, --Orginal Type <class 'list'> Un-needed as it's just a short version of colors
                    names TEXT, --Orginal Type <class 'NoneType'> This will have to be a JSON of {'names': [NAMES]}
                    type TEXT, --Orginal Type <class 'str'>
                    supertypes TEXT, --Orginal Type <class 'list'> This should be a comma seperated list of all the values
                    subtypes TEXT, --Orginal Type <class 'list'>  This should be a comma seperated list of all the values
                    types TEXT, --Orginal Type <class 'list'> This should be a comma seperated list of all the values
                    rarity TEXT, --Orginal Type <class 'str'>
                    "text" TEXT, --Orginal Type <class 'str'>
                    flavor TEXT, --Orginal Type <class 'NoneType'>
                    artist TEXT, --Orginal Type <class 'str'>
                    "number" TEXT, --Orginal Type <class 'str'>
                    "power" TEXT, --Orginal Type <class 'str'>
                    toughness TEXT, --Orginal Type <class 'str'>
                    loyalty INTEGER, --Orginal Type <class 'NoneType'>
                    multiverse_id TEXT, --Orginal Type <class 'NoneType'>
                    variations TEXT, --Orginal Type <class 'NoneType'> I think this will be a comma seperated list of values
                    watermark TEXT, --Orginal Type <class 'NoneType'> I have no idea what this is
                    border TEXT, --Orginal Type <class 'NoneType'>
                    timeshifted TEXT, --Orginal Type <class 'NoneType'>
                    hand TEXT, --Orginal Type <class 'NoneType'>
                    life TEXT, --Orginal Type <class 'NoneType'>
                    release_date TEXT, --Orginal Type <class 'str'>
                    starter TEXT, --Orginal Type <class 'NoneType'>
                    printings TEXT, --Orginal Type <class 'list'>
                    original_text TEXT, --Orginal Type <class 'NoneType'>
                    original_type TEXT, --Orginal Type <class 'NoneType'>
                    "source" TEXT, --Orginal Type <class 'str'>
                    image_url TEXT, --Orginal Type <class 'NoneType'>
                    "set" TEXT, --Orginal Type <class 'str'>
                    set_name TEXT, --Orginal Type <class 'str'>
                    id TEXT PRIMARY KEY, --Orginal Type <class 'str'>
                    legalities TEXT, --Orginal Type <class 'list'>
                    rulings TEXT, --Orginal Type <class 'list'> This will have to be a JSON type of {'rulings' : []}
                    foreign_names TEXT --Orginal Type <class 'list'> This will have to be a JSON type of {'foreign_name' : []}
                    )
'''
#The order in this array must match the order in the above SQL to allow for easier inserts.
MTG_CARDS_KEY_ORDER = ("name", "layout", "mana_cost", "cmc", "colors", "names", "type", "supertypes",
                        "subtypes", "types", "rarity", "text", "flavor", "artist", "number", "power",
                        "toughness", "loyalty", "multiverse_id", "variations", "watermark", "border",
                        "timeshifted", "hand", "life",  "release_date", "starter", "printings", "original_text",
                        "original_type", "source", "image_url", "set", "set_name", "id", "legalities",
                        "rulings", "foreign_names")


COLLECTION_TABLE = '''CREATE TABLE "{}"
                    ("id" TEXT, --The id matching a card id stored in the MTG_CARDS
                    "quantity" INTEGER, --The number of cards in the collection
                    PRIMARY KEY(id),
                    FOREIGN KEY (id) REFERENCES ''' + MTG_CARDS_TABLE_NAME + '''(id)
                    )'''

COLLECTION_LIST_TABLE_NAME = 'collections'
COLLECTION_LIST_TABLE = '''CREATE TABLE ''' + COLLECTION_LIST_TABLE_NAME + '''
                    ("unqkey" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "path" TEXT, --The path of the collection so if name was elves under deck pauper the path would be, deck/pauper/elves
                    "name" TEXT, --The name of the collection
                    "format" TEXT) --The format the collection is legal in, this will only really do anything under decks. '''
COLLECTION_LIST_KEYS = ('unqkey', 'path', 'name', 'format')

class Store:
    def __init__(self):
        self.__dbfile = ''
        self.__dirty = False
        self.openDB = None

    def open_file(self, dbfile):
        try:
            self.openDB.close()
        except Exception:
            pass
        self.openDB = sql.connect(dbfile)

    def create_new_db(self, dbfile):
        '''
        This will create a new database file with the tables of ''' + MTG_CARDS + ''' and ''' + COLLECTION_LIST_TABLE_NAME + '''

        Parameters:
            dbfile : str being the file path of the new database file.
        '''
        try:
            self.openDB.close()
        except Exception: #We're assuming there's nothing loaded.
            pass
        self.dbfile = dbfile
        self.openDB = sql.connect(self.dbfile)
        self.createtable(MTG_CARDS)
        self.createtable(COLLECTION_LIST_TABLE)

    def create_new_collection(self, path, name, format=None):
        '''
        This will create a new table of COLLECTION_TABLE with the table name matching the value
        of parameter name.

        Parameters:
            name : str being the name of the table

            path : str The location of the collection without the name attached

            format : The format the collection is legal in, this will only really do anything under decks.
        '''
        self.createtable(COLLECTION_TABLE.format(name))
        self.insertcollection(path, name, format)

    def collection_exists(self, path, name):
        x = self.openDB.execute('SELECT * FROM ' + COLLECTION_LIST_TABLE_NAME + ' WHERE path=:path and name=:name', {'path':path, 'name':name}).fetchall()
        print('COLLECTION', x)
        return bool(len(x))

    def get_collection_by_name(self, name):
        return bool(len(self.openDB.execute('SELECT * FROM ' + COLLECTION_LIST_TABLE_NAME + ' WHERE name=:name', {'name':name}).fetchall()))

    def insertcollection(self, path, name, format=None):
        '''
        This will add the collection information to the ''' + COLLECTION_LIST_TABLE_NAME + ''' table.

        Parameters:
            name : str being the name of the table

            path : str The location of the collection without the name attached

            format : The format the collection is legal in, this will only really do anything under decks.
        '''
        cur = self.openDB.cursor()
        cur.execute('INSERT INTO ' + COLLECTION_LIST_TABLE_NAME + ' VALUES (?, ?, ?, ?)', (None, path, name, format))
        self.openDB.commit()

    def insert_into_collection(self, path, name, cards):
        tables = self.gettables()
        if not (name in tables):
            self.create_new_collection(path, name)
        cur = self.openDB.cursor()
        for c in cards:
            print(c.name, c.set, c.id)
            cur.execute('INSERT INTO ' + name + ' VALUES (?, ?)', (c.id, 1))
        self.openDB.commit()

    def createtable(self, sql):
        cur = self.openDB.cursor()
        cur.execute(sql)
        self.openDB.commit()

    def gettables(self):
        tables = self.openDB.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        reVal = []
        for t in tables:
            reVal.extend(t)
        return reVal

    def load_collection(self, name):
        cur = self.openDB.execute('select * from '+MTG_CARDS_TABLE_NAME+', '+name+' WHERE '+name+'.id='+MTG_CARDS_TABLE_NAME+'.id;')
        return self.get_all_cards(cur)

    def get_table_items(self, tablename):
        if self.get_collection_by_name(tablename):
            return self.load_collection(tablename)
        else:
            cur = self.openDB.cursor()
            cur.execute('select * from '+tablename)
            return self.get_all_cards(cur)
        return []

    def get_collection_information(self):
        return self.openDB.cursor().execute('select * from '+COLLECTION_LIST_TABLE_NAME).fetchall()

    def result_to_dict(self, result, columns=MTG_CARDS_KEY_ORDER):
        re = {}
        c = 0
        while c < len(result): #I really need to fix this mess....I hate this
            key = columns[c]
            val = result[c]
            if val == 'NULL':
                re[key] = None
            elif key in ['colors', 'supertypes', 'subtypes', 'types', 'variations', 'printings']:
                re[key] = val.split(',')
            elif key in ['names','rulings', 'foreign_name', 'legalities']:
                re[key] = json.loads(val)[key]
            elif key in   ['name', 'layout', 'mana_cost', 'type', 'rarity', 'text', 'flavor', 'artist',
                        'number', 'power', 'toughness', 'multiverse_id', 'watermark', 'border',
                        'timeshifted', 'hand', 'life', 'release_date', 'starter', 'printings',
                        'original_text', 'original_type', 'source', 'image_url', 'set', 'set_name',
                        'id', 'foreign_names']:
                re[key] = val
            elif key in ['cmc', 'loyalty']:
                re[key] = int(val)
            c += 1
        return re

    def getcard(self, result, columns=MTG_CARDS_KEY_ORDER):
        return CardItem(self.result_to_dict(result, columns))

    def get_all_cards(self, cursor):
        re = []
        col = [d[0] for d in cursor.description]
        for c in cursor.fetchall():
            re.append(self.getcard(c, col))
        return re

    def listvalues(self, card): #I think there's at least one bug here with variations
        reLst = []
        for k in MTG_CARDS_KEY_ORDER:
            v = getattr(card, k)
            if v is None and k != 'id':
                reLst.append('NULL')
            elif k == 'id' and v is None: #id being the primary key don't allow this to be empty.
                raise ValueError('Primary key of id can not be None, must be a string')
            elif k in ['colors', 'supertypes', 'subtypes', 'types', 'printings']:
                reLst.append(','.join(v))
            elif k in ['names','rulings', 'foreign_name', 'legalities']:
                reLst.append(json.dumps({k:v}))
            elif k in   ['name', 'layout', 'mana_cost', 'type', 'rarity', 'text', 'flavor', 'artist',
                        'number', 'power', 'toughness', 'multiverse_id', 'watermark', 'border',
                        'timeshifted', 'hand', 'life', 'release_date', 'starter',
                        'original_text', 'original_type', 'source', 'variations', 'image_url', 'set', 'set_name',
                        'id', 'foreign_names']:
                reLst.append(str(v))
            elif k in ['cmc', 'loyalty', 'quantity']:
                reLst.append(int(v))
            else: #If we get this fair then whelp you're on your own
                raise KeyError('Unknown key '+k)
        return reLst

    def insertcardstatement(self):
        return  'INSERT INTO '+ MTG_CARDS_TABLE_NAME + ' VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'

    def insertcards(self, cards):
        cds = cards
        if not isinstance(cards, (tuple, list)):
            cds = [cards]
        cur = self.openDB.cursor()
        for c in cds:
            l = self.listvalues(c)
            try:
                cur.execute(self.insertcardstatement(), l)
            except sql.IntegrityError: #ID is probably already in the database
                pass
        self.openDB.commit()

    def wherestatement(self, **kwargs):
        reStr = ''
        for k, v in kwargs.items():
            reStr += k + ' LIKE "%' + v + '%" '
        return reStr

    def getcards(self, table=MTG_CARDS_TABLE_NAME, **kwargs):
        cur = self.openDB.cursor()
        cur.execute('select * from '+table+' where '+self.wherestatement(**kwargs))
        return self.get_all_cards(cur)

    def get_cards_exact(self, table=MTG_CARDS_TABLE_NAME, **kwargs):
        cur = self.openDB.cursor()
        reStr = []
        for k, v in kwargs.items():
            reStr.append('"' + k + '" = "' + v + '"')
        cur.execute('select * from '+table+' where '+' and '.join(reStr)+' ; ')
        return self.get_all_cards(cur)

    def query_all_cards(self, queries):
        '''
        To make up for the inaccuracy of mtgsdk queries we will need to query for a lot of cards
        get the results and store them into the mtgcards table. Once this is accomplished then we can
        create more accurate queries on the sqlite database.

        Params:
            queries : dict
                This should be a dictionary where the keys are the set_names and the value should be
                a list of card names.
        '''
        urlen = len(__endpoint__ + CardItem.RESOURCE)
        for k, v in queries.items():
            curlen = urlen + len(k)
            curnames = []
            for n in v:
                if (1+len(n)+curlen) < URL_LENGTH:
                    curnames.append(n)
                else:
                    print('1 SET ', k, ' LEN ', len(curnames))
                    cards += self.query_and_add(name='|'.join(curnames), set_name=k)
                    curnames = []
            if len(curnames):
                c = self.query_and_add(name='|'.join(curnames), set_name=k)
                print('2 SET ', k, ' LEN ', len(curnames), 'RETURNING ', len(c))

    def query_and_add(self, **kwargs):
        cards = QueryBuilder(CardItem).where(**kwargs).all()
        self.insertcards(cards)
        return cards

    def csvr(self, csvfile): #This function is god awful
        wheres = QueryBuilder(CardItem)
        queries = {}
        cards = []
        res = readtcgplayercsv(csvfile)
        totals = {}
        for r in res:
            allc = self.get_cards_exact(name=r['Name'], set_name=r['Set'])

            if len(allc):
                print('GOT THIS MANY ', len(allc), r['Name'], r['Set'])
                cards += allc
                try:
                    totals[allc[0].id].quantity += 1
                except KeyError:
                    totals[allc[0].id] = allc[0]
            else:
                try:
                    queries[r['Set']].append(r['Name'])
                except KeyError:
                    queries[r['Set']] = [r['Name']]
        self.query_all_cards(queries) #Query into mtgsdk then we'll have to requery back into sqlite

        for k, n in queries.items():
            for cn in n:
                allc = self.get_cards_exact(name=cn, set_name=k)
                if len(allc):
                    cards += allc
                    try:
                        totals[allc[0].id].quantity += 1
                    except KeyError:
                        totals[allc[0].id] = allc[0]
                else:
                    pass
                    #try:
                        #queries[k].append(cn)
                    #except KeyError:
                        #queries[k] = cn
        print('RETURNING LEN ', len(cards), 'QUERIES LEN ', len(queries.keys()))
        return list(totals.values())
        #return wheres.where(name='|'.join(names), set='|'.join(sets)).all()

    def __get_dbfile(self):
        return self.__dbfile

    def __set_dbfile(self, newfile):
        self.__dbfile = newfile
    dbfile = property(__get_dbfile, __set_dbfile)

    @property
    def dirty(self):
        return self.__dirty

def readtcgplayercsv(csvfile):
    reDict = []
    dcsv = csv.DictReader(open(csvfile))
    for r in dcsv:
        reDict.append(r)
    return reDict

def old(*args):
    from mtgsdk import Card
    store = Store('./tester.mtg')
    #try:
        #store.createtable(MTG_CARDS)
    #except Exception:
        #pass
    #store.insertcards(Card.where(types='creature').where(subtypes='elf').where(colors='black').all())
    store.crea_collection_tetable('maincollection')
    import pprint
    pprint.pprint(store.getcards(colors='Green'))
    store.openDB.close()


if __name__ == '__main__':
    csvr()
