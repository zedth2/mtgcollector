#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

from datetime import datetime
from json import dumps, loads
from collections import OrderedDict

CONVERSION_TO_Py = {'str': lambda k, v: str(v),
                    'epoch': lambda k, v: datetime.fromtimestamp(v),
                    'csv' : lambda k, v: v.split(','),
                    'json' : lambda k, v: loads(v)[k],
                    'bool' : lambda k, v: bool(v),
                    'int' : lambda k, v: int(v),
                    'real' : lambda k, v: float(v),
                   }

CONVERSION_TO_SQL = {'str': lambda k, v: str(v),
                    'epoch': lambda k, v: datetime.timestamp(v),
                    'csv' : lambda k, v: ','.join(v),
                    'json' : lambda k, v: dumps({k:v}),
                    'bool' : lambda k, v: v,
                    'int' : lambda k, v: v,
                    'real' : lambda k, v: v,
                   }

MTGCARDS_TABLE_NAME = 'mtgcards'
MTGCARDS_KEYS_TYPES = OrderedDict([
                ("id", 'str'),
                ("multiverse_id", 'int' ),
                ("collectors_number", 'str' ),
                ("name", 'str' ),
                ("set_code", 'str' ),
                ("color", 'csv' ),
                ("mana_cost", 'str' ),
                ("cmc", 'real' ),
                ("rarity", 'str' ),
                ("power", 'str' ),
                ("toughness", 'str' ),
                ("loyalty", 'str' ),
                ("flavor_text", 'str' ),
                ("type_line", 'str' ),
                ("oracle_text", 'str' ),
                ("artist", 'str' ),
                ("layout", 'str' ),
                ("types", 'csv' ),
                ("subtypes", 'csv' ),
                ("supertypes", 'csv' ),
                ("foreign_names", 'json' ),
                ("rulings", 'json' ),
                ("legalities", 'json' ),
                ("image_url", 'str' )])
                #("language", 'str' )])
MTGCARDS_PRIMARY = tuple(MTGCARDS_KEYS_TYPES.keys())[0] #--A hash being sha1(card_name, set_name, multiverse_id, collectors_number)
MTGCARDS_SQL = '''CREATE TABLE ''' + MTGCARDS_TABLE_NAME + '''
                (
                "id" TEXT PRIMARY KEY,
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
                FOREIGN KEY("set_code") REFERENCES mtgsets("code")
                )
'''

MTGSETS_TABLE_NAME = 'mtgsets'
MTGSETS_KEYS = ('code', 'name', 'block', 'border', 'gatherer_code', 'release_date', 'booster', 'online_only')
MTGSETS_KEYS_TYPES = OrderedDict([
                    ("code", 'str' ),
                    ("name", 'str' ),
                    ("block", 'str' ),
                    ("border", 'str' ),
                    ("gatherer_code", 'str' ),
                    ("release_date", 'epoch' ),
                    ("booster", 'json' ),
                    ("online_only", 'bool' )])

MTGSETS_PRIMARY = tuple(MTGSETS_KEYS_TYPES.keys())[0]
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
#MTG_USERBUILD_KEYS = ('unqkey', 'path', 'name', 'format', 'type')
MTG_USERBUILD_KEYS_TYPES = OrderedDict([
                            ('unqkey', 'int'),
                            ('path', 'str'),
                            ('name', 'str'),
                            ('format', 'str'),
                            ('type', 'str')])

MTG_USERBUILD_SQL = '''CREATE TABLE ''' + MTG_USERBUILD_TABLE_NAME + '''
        ("unqkey" INTEGER PRIMARY KEY AUTOINCREMENT,
        "path" TEXT, --The path of the collection so if name was elves under deck pauper the path would be, deck/pauper/elves
        "name" TEXT, --The name of the collection
        "format" TEXT, --The format the collection is legal in, this will only really do anything under decks.
        "type" TEXT) --Should be either deck or collection'''


COLLECTION_KEYS = ('id', 'count')
DECK_KEYS = ('id', 'count', 'board')


def collection_sql(tablename):
    return '''CREATE TABLE {}
                (
                "id" TEXT PRIMARY KEY,
                "count" INTEGER,
                FOREIGN KEY("id") REFERENCES {}("id")
                )'''.format(tablename, MTGCARDS_TABLE_NAME)

def deck_sql(tablename):
    return '''CREATE TABLE {}
                (
                "id" TEXT PRIMARY KEY,
                "count" INTEGER,
                "board" BOOLEAN,
                FOREIGN KEY("id") REFERENCES {}("id")
                )'''.format(tablename, MTGCARDS_TABLE_NAME)
