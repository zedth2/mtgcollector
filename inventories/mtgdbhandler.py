#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

import sqlite3 as sql
from datetime import datetime
import logging

from . import Set, Card, Collection, Deck, get_class
from .sqlments import *
from .externalapis.mtgsdkreader import where_card, where_set, find_many_cards
from .externalapis import scryfalldealer

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

    def find_by_like(self, table, item_type, **kwargs):
        cur = self.openDB.cursor()
        reSets = []
        return self.get_items(cur.execute('select * from ' + table + ' where ' + self.where_like_statement(**kwargs)), item_type)

    def find_by_exact(self, table, item_type, **kwargs):
        wheres = []
        for k, v in kwargs.items():
            wheres.append('"' + k + '" = "' + v + '"')
        statement = 'SELECT * FROM '+table + ' WHERE ' + ' and '.join(wheres) + '; '
        return self.get_items(self.openDB.execute(statement), item_type)

    def get_items(self, cursor, item_type):
        sets = []
        for vals in cursor.fetchall():
            sets.append(item_type.from_db_values(vals))
        return sets

    def where_like_statement(self, **kwargs):
        reStr = ''
        for k, v in kwargs.items():
            reStr += k + ' LIKE "%' + v + '%" '
        return reStr

#Set handlers Begin..
    def find_sets_by_like(self, **kwargs):
        return self.find_by_like(MTGSETS_TABLE_NAME, Set, **kwargs)

    def find_sets_exact(self, **kwargs):
        return self.find_by_exact(MTGSETS_TABLE_NAME, Set, **kwargs)

    def all_set_codes(self):
        result = self.openDB.execute('SELECT set_code FROM '+MTGSETS_TABLE_NAME).fetchall()
        reLst = []
        for r in result:
            reLst.extend(r)
        return reLst

    def all_sets(self):
        return [Set.from_db_values(r) for r in self.openDB.execute('SELECT * FROM ' + MTGSETS_TABLE_NAME).fetchall()]

    def insert_sets(self, sets):
        if not isinstance(sets, (tuple, list)):
            sets = [sets]
        inserts = [s.get_db_values() for s in sets]
        cursor = self.openDB.cursor()
        cursor.executemany('INSERT INTO ' + MTGSETS_TABLE_NAME + ' VALUES ('+', '.join(['?']*len(MTGSETS_KEYS_TYPES.keys())) + ');', inserts)
        self.openDB.commit()

    def get_all_cards_from_set(self, set):
        return self.find_cards_exact(set_code=set.set_code)
#..End Set handlers

#Card handlers Begin...
    def find_cards_by_like(self, **kwargs):
        return self.find_by_like(MTGCARDS_TABLE_NAME, Card, **kwargs)

    def find_cards_exact(self, **kwargs):
        return self.find_by_exact(MTGCARDS_TABLE_NAME, Card, **kwargs)


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
                logging.debug("Failure NO FIND to find {}".format(c.name))
                fails.append(c)
            else:
                cnt = 0
                while len(finds) > cnt:
                    finds[cnt].count = c.count
                    cnt += 1
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
            #self.insert_cards(find_many_cards(fails))
            self.insert_cards(scryfalldealer.find_cards_by_name(fails))
            success, fails = self.find_cards_from_cards(cards)
        return success, fails
#...End Card handlers

#Userbuild handlers Begin...
    def insert_userbuild(self, name, path, type, retype, format=None, cards=[]):
        cursor = self.openDB.cursor()
        cursor.execute('INSERT INTO ' + MTG_USERBUILD_TABLE_NAME + ' VALUES (' + ', '.join(['?']*len(MTG_USERBUILD_KEYS_TYPES.keys())) + ');', (None, path, name, format, type, None))
        rowid = cursor.lastrowid
        self.openDB.commit()
        coll = self.get_userbuild(name, path, retype, rowid)[0]
        cursor.execute('UPDATE ' + MTG_USERBUILD_TABLE_NAME + ' SET tablename = "' + coll.tablename + '" WHERE unqkey = ' + str(coll.unqkey) + ';')
        cursor.execute(retype.sql_create_table()(coll.tablename))
        self.openDB.commit()
        coll.cards = cards
        self.insert_cards_userbuild(coll)
        return coll

    def get_userbuild(self, name, path, retype, unqkey=None):
        reLst = []
        cols = []
        if unqkey is None:
            cols = self.openDB.execute('SELECT * FROM ' + MTG_USERBUILD_TABLE_NAME + ' WHERE "name" = :name AND "path" = :path AND type = :collection', {"name":name, "path": path, "collection": retype.collection_type()}).fetchall()
        else:
            cols = self.openDB.execute('SELECT * FROM ' + MTG_USERBUILD_TABLE_NAME + ' WHERE "name" = :name AND "path" = :path AND type = :collection AND unqkey = :unqkey', {"name":name, "path": path, "collection": retype.collection_type(), "unqkey": unqkey}).fetchall()
        for c in cols:
            reLst.append(retype.from_db_values(c))
        return reLst

    def insert_cards_userbuild(self, collection):
        inserts = collection.get_card_inserts()
        cursor = self.openDB.cursor()
        try:
            cursor.executemany('INSERT INTO ' + collection.tablename + ' VALUES (' + ', '.join(['?']*len(collection.__class__.database_keys())) + ');', inserts)
        except sql.IntegrityError as ex:
            print(ex)
        self.openDB.commit()

    def get_all_userbuilds(self):
        collections = []
        typeindex = list(MTG_USERBUILD_KEYS_TYPES.keys()).index('type')
        cursor = self.openDB.cursor()
        for r in cursor.execute('SELECT * FROM ' + MTG_USERBUILD_TABLE_NAME + ';').fetchall():
            collections.append(get_class(r[typeindex]).from_db_values(r))
            collections[-1].cards = self.get_cards_from_collection(collections[-1])
        return collections
#...End Userbuild handlers

    def create_collection(self, name, path, cards=[]):
        return self.insert_userbuild(name, path, Collection.collection_type(), Collection, None, cards)


    def get_cards_from_collection(self, collection): #select * from mtgcards join Pauper using (id);
        if not collection.tablename:
            raise ValueError('Collection must contain a table name')
        keytypes = {}
        keytypes.update(MTGCARDS_KEYS_TYPES)
        keytypes.update(collection.database_keytypes())
        cursor = self.openDB.execute('SELECT * FROM ' + MTGCARDS_TABLE_NAME + ' join ' + collection.tablename + ' using (id);')
        cards = []
        for c in cursor.fetchall():
            cards.append(Card.from_db_values(c, keytypes))
        return cards

    def create_deck(self, name, path, format='kitchen', cards=[]):
        return self.insert_userbuild(name, path, Deck.collection_type(), Deck, format, cards)

    def create_qube(self, name, path):
        cursor = self.openDB.cursor()
        cursor.execute('INSERT INTO ' + MTG_USERBUILD_TABLE_NAME + ' VALUES (' + ', '.join(['?']*len(MTG_USERBUILD_KEYS_TYPES.keys())) + ');', (None, path, name, None, 'QUBE'))
        cursor.execute(deck_sql(name))
        self.openDB.commit()

if __name__ == '__main__':
    store = MTGDatabaseHandler()
    store.create_new_db('./fuckkkk.mtg')
