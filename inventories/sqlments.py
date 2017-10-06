#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

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
MTGSETS_PRIMARY = MTGSETS_KEYS[0]
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
