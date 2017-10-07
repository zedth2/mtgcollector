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

    def find_set_by_exact(self, **kwargs):
        sets = []
        wheres = []
        for k, v in kwargs:
            wheres.append('"' + k + '" = "' + v + '"')
        statement = 'SELECT * FROM '+MTGSETS_TABLE_NAME + ' WHERE ' + ' and '.join(wheres) + '; '
        for vals in self.openDB.execute(statement).fetchall():
            sets.append(Set.from_db_values(MTGSETS_KEYS, vals))
        return sets

    def insert_sets(self, sets):
        if not isinstance(sets, (tuple, list)):
            sets = [sets]
        inserts = [s.get_db_values(MTGSETS_KEYS) for s in sets]
        cursor = self.openDB.cursor()
        cursor.executemany('INSERT INTO ' + MTGSETS_TABLE_NAME + ' VALUES ('+', '.join(['?']*len(MTGSETS_KEYS)) + ');', inserts)
        self.openDB.commit()


if __name__ == '__main__':
    store = MTGDatabaseHandler()
    store.create_new_db('./fuckkkk.mtg')
