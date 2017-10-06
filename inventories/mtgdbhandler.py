#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

import sqlite3 as sql
from datetime import datetime
from . import Set, Card

MTGCARDS_TABLE_NAME = 'mtgcards'
MTGCARDS_KEYS = ("id", "multiverse_id", "collectors_number", "name", "color", "mana_cost",
                "cmc", "rarity", "power", "toughness", "loyalty", "flavor_text", "type_line",
                "oracle_text", "artist", "layout", "types", "subtypes", "supertypes", "foreign_names",
                "rulings", "legalities", "image_url", "language")
MTGCARDS_SQL = '''CREATE TABLE ''' + MTGCARDS_TABLE_NAME + '''
                (
                "id" TEXT PRIMARY KEY, --A hash being sha1(card_name, set_name, multiverse_id, collectors_number)
                "multiverse_id" INTEGER,
                "collectors_number" TEXT,
                "name" TEXT,
                "set_code" TEXT,
                "color" TEXT,
                "mana_cost" TEXT,
                "cmc" REAL,
                "rarity" TEXT,
                "power" TEXT,
                "toughness" TEXT,
                "loyalty" TEXT,
                "flavor_text" TEXT,
                "type_line" TEXT,
                "oracle_text" TEXT,
                "artist" TEXT,
                "layout" TEXT,
                "types" TEXT,
                "subtypes" TEXT,
                "supertypes" TEXT,
                "foreign_names" TEXT,
                "rulings" TEXT,
                "legalities" TEXT,
                "image_url" TEXT,
                "language" TEXT,
                FOREIGN KEY("set_code") REFERENCES mtgsets("code")
                )
'''

MTGSETS_TABLE_NAME = 'mtgsets'
MTGSETS_KEYS = ('code', 'name', 'block', 'border', 'gatherer_code', 'release_date', 'booster', 'online_only')
MTGSETS_SQL = '''CREATE TABLE ''' + MTGSETS_TABLE_NAME + '''
                (
                "code" TEXT PRIMARY KEY,
                "name" TEXT,
                "block" TEXT,
                "border" TEXT,
                "gatherer_code" TEXT,
                "release_date" INTEGER,
                "booster" TEXT,
                "online_only" BOOLEAN
                )
'''

MTG_USERBUILD_TABLE_NAME = 'userbuilds'
MTG_USERBUILD_KEYS = ('unqkey', 'path', 'name', 'format', 'type')

COLLECTION_KEYS = ('id', 'count')
DECK_KEYS = ('id', 'count', 'board')

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
        self.openDB.executemany('INSERT INTO ' + MTGSETS_TABLE_NAME + ' VALUES '+', '.join(['?']*len(MTGSETS_KEYS)), inserts)
        self.openDB.commit()

if __name__ == '__main__':
    store = MTGDatabaseHandler()
    store.create_new_db('./fuckkkk.mtg')
