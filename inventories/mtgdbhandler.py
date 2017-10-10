#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

import sqlite3 as sql
from datetime import datetime
from . import Set, Card, Collection, Deck
from .sqlments import *
from .externalapis.mtgsdkreader import where_card, where_set, find_many_cards

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
        cur.execute(MTGCARDS_SQL)
        cur.execute(MTG_USERBUILD_SQL)
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
        return self.find_by_like(MTGCARDS_TABLE_NAME, MTGCARDS_KEYS_TYPES, Card, **kwargs)

    def find_cards_exact(self, **kwargs):
        return self.find_by_exact(MTGCARDS_TABLE_NAME, MTGCARDS_KEYS_TYPES, Card, **kwargs)

    def insert_sets(self, sets):
        if not isinstance(sets, (tuple, list)):
            sets = [sets]
        inserts = [s.get_db_values() for s in sets]
        cursor = self.openDB.cursor()
        cursor.executemany('INSERT INTO ' + MTGSETS_TABLE_NAME + ' VALUES ('+', '.join(['?']*len(MTGSETS_KEYS_TYPES.keys())) + ');', inserts)
        self.openDB.commit()

    def insert_cards(self, cards):
        if not isinstance(cards, (tuple, list)):
            cards = [cards]
        inserts = [c.get_db_values() for c in cards]
        cursor = self.openDB.cursor()
        cursor.executemany('INSERT INTO ' + MTGCARDS_TABLE_NAME + ' VALUES (' + ', '.join(['?']*len(MTGCARDS_KEYS_TYPES.keys())) + ');', inserts)
        self.openDB.commit()

    def find_cards_by_like_to_external(self, **kwargs):
        '''
        This is only going to work for single items. The or of `|` won't find anything in the local
        sqlite DB.
        '''
        cards = self.find_cards_by_like(**kwargs)
        if 0 == len(cards):
            cards = where_card(**kwargs)
            self.insert_cards(cards)
        return self.find_cards_by_like(**kwargs)

    def find_cards_exact_to_external(self, **kwargs):
        '''
        This is only going to work for single items. The or of `|` won't find anything in the local
        sqlite DB.
        '''
        cards = self.find_cards_exact(**kwargs)
        if 0 == len(cards):
            cards = where_card(**kwargs)
            self.insert_cards(cards)
        return self.find_cards_exact(**kwargs)

    def find_cards_from_cards(self, cards):
        fails = []
        success = []
        for c in cards:
            finds = []
            if c.name is not None and c.set_code is not None:
                finds = self.find_cards_exact(name=c.name, set_code=c.set_code)
            elif c.name is not None:
                finds = self.find_cards_exact(name=c.name)
            else:
                fails.append(c)
            if 0 == len(finds):
                fails.append(c)
            else:
                success += finds
        return success, fails

    def find_cards_from_cards_external(self, cards):
        '''
        Pass in a list of cards to find. Will query locally to find what cards are already in the local
        database. Any cards not found in the DB will be passed to a mtgsdk querier to find there.
        Those will be inserted into the local DB and then requeried locally.

        Exceptions: ValueError passed up from externalapis.mtgsdkreader.find_many_cards

        Return: a tuple being (list, list) each list is a list of cards. Index 0 is the cards found.
                Index 1 is the cards passed in but not found.
        '''
        success, fails = self.find_cards_from_cards(cards)
        if 0 < len(fails):
            self.insert_cards(find_many_cards(fails))
            success, fails = self.find_cards_from_cards(cards)
        return success, fails


    def find_many_cards_external(self, cards):
        finds = []
        for c in cards:
            name_query

    def create_collection(self, name, path):
        cursor = self.openDB.cursor()
        cursor.execute('INSERT INTO ' + MTG_USERBUILD_TABLE_NAME + ' VALUES (' + ', '.join(['?']*len(MTG_USERBUILD_KEYS_TYPES.keys())) + ');', (None, path, name, None, 'COLLECTION'))
        cursor.execute(collection_sql(name))
        self.openDB.commit()
        return self.get_collection(name, path)

    def get_collection(self, name, path):
        cursor = self.openDB.cursor()
        cols = cursor.execute('SELECT * FROM ' + MTG_USERBUILD_TABLE_NAME + ' WHERE "name" = :name AND "path" = :path AND "type" = :collection', {"name":name, "path": path, "collection":'COLLECTION'}).fetchall()
        reCol = []
        for c in cols:
            reCol.append(Collection.from_db_values(c))
        return reCol

    def create_deck(self, name, path):
        cursor = self.openDB.cursor()
        cursor.execute('INSERT INTO ' + MTG_USERBUILD_TABLE_NAME + ' VALUES (' + ', '.join(['?']*len(MTG_USERBUILD_KEYS_TYPES.keys())) + ');', (None, path, name, 'kitchen', 'DECK'))
        cursor.execute(deck_sql(name))
        self.openDB.commit()

    def create_qube(self, name, path):
        cursor = self.openDB.cursor()
        cursor.execute('INSERT INTO ' + MTG_USERBUILD_TABLE_NAME + ' VALUES (' + ', '.join(['?']*len(MTG_USERBUILD_KEYS_TYPES.keys())) + ');', (None, path, name, None, 'QUBE'))
        cursor.execute(deck_sql(name))
        self.openDB.commit()

if __name__ == '__main__':
    store = MTGDatabaseHandler()
    store.create_new_db('./fuckkkk.mtg')
