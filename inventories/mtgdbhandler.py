#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

import sqlite3 as sql
from datetime import datetime
from . import Set, Card
from .sqlments import *

class MTGDatabaseHandler:
    def __init__(self):
        self.__dbfile = ''
        self.__dirty = False
        self.openDB = None

    def open_file(self, dbfile):
        self.close_db_no_error()
        self.openDB = sql.connect(dbfile)
        self.dbfile = dbfile

    def create_new_db(self, dbfile):
        '''

        '''
        self.close_db_no_error()
        self.open_file(dbfile)
        cur = self.openDB.cursor()
        cur.execute(MTGSETS_SQL)
        #cur.execute(MTGCARDS_SQL)
        self.openDB.commit()

    def close_db_no_error(self):
        try:
            self.openDB.close()
        except Exception:
            pass

    def gettables(self):
        tables = self.openDB.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        reVal = []
        for t in tables:
            reVal.extend(t)
        return reVal

    def find_by_exact(self, table, keys, item_type, **kwargs):
        wheres = []
        for k, v in kwargs.items():
            wheres.append('"' + k + '" = "' + v + '"')
        statement = 'SELECT * FROM '+table + ' WHERE ' + ' and '.join(wheres) + '; '
        return self.get_items(self.openDB.execute(statement), item_type, keys)

    def get_items(self, cursor, item_type, keys):
        sets = []
        for vals in cursor.fetchall():
            sets.append(item_type.from_db_values(vals))
        return sets

    def wherestatement(self, **kwargs):
        reStr = ''
        for k, v in kwargs.items():
            reStr += k + ' LIKE "%' + v + '%" '
        return reStr

    def find_by_like(self, table, keys, item_type, **kwargs):
        cur = self.openDB.cursor()
        reSets = []
        return self.get_items(cur.execute('select * from ' + table + ' where ' + self.wherestatement(**kwargs)), item_type, keys)

    def find_sets_by_like(self, **kwargs):
        return self.find_by_like(MTGSETS_TABLE_NAME, MTGSETS_KEYS_TYPES, Set, **kwargs)

    def find_sets_exact(self, **kwargs):
        return self.find_by_exact(MTGSETS_TABLE_NAME, MTGSETS_KEYS_TYPES, Set, **kwargs)

    def find_cards_by_like(self, **kwargs):
        return self.find_by_like(MTGCARDS_TABLE_NAME, MTGCARDS_KEYS, Card, **kwargs)

    def find_cards_exact(self, **kwargs):
        return self.find_by_exact(MTGCARDS_TABLE_NAME, MTGCARDS_KEYS, Card, **kwargs)

    def insert_sets(self, sets):
        if not isinstance(sets, (tuple, list)):
            sets = [sets]
        inserts = [s.get_db_values() for s in sets]
        cursor = self.openDB.cursor()
        cursor.executemany('INSERT INTO ' + MTGSETS_TABLE_NAME + ' VALUES ('+', '.join(['?']*len(MTGSETS_KEYS_TYPES.keys())) + ');', inserts)
        self.openDB.commit()

if __name__ == '__main__':
    store = MTGDatabaseHandler()
    store.create_new_db('./fuckkkk.mtg')
