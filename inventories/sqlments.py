#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

from datetime import datetime
from json import dumps, loads
from collections import OrderedDict

TYPE_MAP_Py_To_SQL = {'str': 'TEXT',
                    'epoch': 'INTEGER',
                    'csv' : 'TEXT',
                    'json' : 'TEXT',
                    'bool' : 'BOOLEAN',
                    'int' : 'INTEGER',
                    'real' : 'REAL',
                   }

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

def table_sql(key_types, tablename, primkey, autoinc=False, extras=''):
    sql = 'CREATE TABLE {} ('.format(tablename)
    prim = ' PRIMARY KEY' + (' AUTOINCREMENT' if autoinc else '')
    for k, t in key_types.items():
        types = TYPE_MAP_Py_To_SQL[t]
        if primkey == k:
            types += prim
        sql += '"{}" {}, '.format(k, types)
    return sql + extras + ');'

MTGCARDS_TABLE_NAME = 'mtgcards'
MTGCARDS_KEYS_TYPES = OrderedDict([
                ("id", 'str' ),
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
                ("type_line", 'str' ),
                ("oracle_text", 'str' ),
                ("artist", 'str' ),
                ("layout", 'str' ),
                ("types", 'csv' ),
                ("subtypes", 'csv' ),
                ("supertypes", 'csv' ),
                ("legalities", 'json' ),
                ("image_url", 'str' ),
                ("extras", 'str'),])
                #("language", 'str' )])
MTGCARDS_PRIMARY = tuple(MTGCARDS_KEYS_TYPES.keys())[0] #--A hash being sha1(card_name, set_name, multiverse_id, collectors_number)
MTGCARDS_EXTRA_SQL = 'FOREIGN KEY("set_code") REFERENCES mtgsets("set_code")'
MTGCARDS_SQL = table_sql(MTGCARDS_KEYS_TYPES, MTGCARDS_TABLE_NAME, MTGCARDS_PRIMARY, False, MTGCARDS_EXTRA_SQL)
#'''CREATE TABLE ''' + MTGCARDS_TABLE_NAME + '''
                #(
                #"id" TEXT PRIMARY KEY,
                #"multiverse_id" INTEGER,
                #"collectors_number" TEXT,
                #"name" TEXT,
                #"set_code" TEXT COLLATE NOCASE,
                #"color" TEXT,
                #"mana_cost" TEXT,
                #"cmc" REAL,
                #"rarity" TEXT,
                #"power" TEXT,
                #"toughness" TEXT,
                #"loyalty" TEXT,
                #"type_line" TEXT,
                #"artist" TEXT,
                #"layout" TEXT,
                #"types" TEXT,
                #"subtypes" TEXT,
                #"supertypes" TEXT,
                #"legalities" TEXT,
                #"image_url" TEXT,
                #"card_face" TEXT,
                #"extras" TEXT,

MTGSETS_TABLE_NAME = 'mtgsets'
#MTGSETS_KEYS = ('code', 'name', 'block', 'border', 'gatherer_code', 'release_date', 'booster', 'online_only')
MTGSETS_KEYS_TYPES = OrderedDict([
                    ("set_code", 'str' ),
                    ("name", 'str' ),
                    ("block", 'str' ),
                    ("border", 'str' ),
                    ("gatherer_code", 'str' ),
                    ("release_date", 'epoch' ),
                    ("online_only", 'bool' ),
                    ("icon_svg_uri", 'str'),
                    ("card_count", 'int'),
                    ("set_type", 'str'),])

MTGSETS_PRIMARY = tuple(MTGSETS_KEYS_TYPES.keys())[0]
MTGSETS_SQL = '''CREATE TABLE ''' + MTGSETS_TABLE_NAME + '''
                (
                "set_code" TEXT PRIMARY KEY COLLATE NOCASE,
                "name" TEXT,
                "block" TEXT,
                "border" TEXT,
                "gatherer_code" TEXT,
                "release_date" INTEGER,
                "online_only" BOOLEAN,
                "icon_svg_uri" TEXT,
                "card_count" INTEGER,
                "set_type" TEXT
                )
'''

MTG_USERBUILD_TABLE_NAME = 'userbuilds'
#MTG_USERBUILD_KEYS = ('unqkey', 'path', 'name', 'format', 'type')
MTG_USERBUILD_KEYS_TYPES = OrderedDict([
                            ('unqkey', 'int'),
                            ('path', 'str'),
                            ('name', 'str'),
                            ('format', 'str'),
                            ('type', 'str'),
                            ('tablename', 'str')])

MTG_USERBUILD_SQL = '''CREATE TABLE ''' + MTG_USERBUILD_TABLE_NAME + '''
        ("unqkey" INTEGER PRIMARY KEY AUTOINCREMENT,
        "path" TEXT, --The path of the collection so if name was elves under deck pauper the path would be, deck/pauper/elves
        "name" TEXT, --The name of the collection
        "format" TEXT, --The format the collection is legal in, this will only really do anything under decks.
        "type" TEXT, --Should be either deck or collection
        "tablename" TEXT)'''


COLLECTION_KEYS_TYPES = OrderedDict([('id', 'str'),
                                    ('count', 'int'),])

def collection_sql(tablename):
    return '''CREATE TABLE "{}"
                (
                "id" TEXT PRIMARY KEY,
                "count" INTEGER,
                FOREIGN KEY("id") REFERENCES {}("id")
                )'''.format(tablename, MTGCARDS_TABLE_NAME)


DECK_KEYS_TYPES = OrderedDict([('id', 'str'),
                                ('count', 'int'),
                                ('board', 'str'),])

def deck_sql(tablename):
    return '''CREATE TABLE "{}"
                (
                "id" TEXT PRIMARY KEY,
                "count" INTEGER,
                "board" TEXT,
                FOREIGN KEY("id") REFERENCES {}("id")
                )'''.format(tablename, MTGCARDS_TABLE_NAME)


def insert_statement(tablename, key_types):
    return ('INSERT INTO "{tablename}" VALUES ('+', '.join(['?']*len(key_types))+');').format(tablename=tablename)
