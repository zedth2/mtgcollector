#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
from hashlib import sha1
from datetime import datetime
from .sqlments import *
import json

import logging

SCRYFALL_COLORS = {'U':'Blue','B':'Black', 'G':'Green', 'W':'White', 'R':'Red'}
class Collection:
    def __init__(self, name, path, unqkey=None, tablename='', type='COLLECTION'):
        self.name = name
        self.path = path
        self.cards = []
        self.__tablename = ''
        self.__unqkey = unqkey
        self.type = type

    def get_card_inserts(self, cards=[]):
        if not len(cards):
            cards = self.cards
        keys = self.__class__.database_keys()
        inserts = []
        for c in cards:
            cur = []
            for k in keys:
                cur.append(c[k])
            inserts.append(tuple(cur))
        return inserts

    def contains(self, card):
        reCard = None
        for c in self.cards:
            if c == card:
                reCard = c
                break
        return reCard

    def __contains__(self, card):
        return card in self.cards

    @property
    def unqkey(self):
        return self.__unqkey

    @property
    def tablename(self):
        if self.unqkey is None:
            raise ValueError('Needs a unqiue key to create a table name')
        if self.__tablename is '':
            table = 'U_' + self.name.replace(' ', '_')
            self.__tablename = self.name.replace(' ', '_') + str(self.unqkey)
        return self.__tablename

    @staticmethod
    def database_keys():
        return tuple(COLLECTION_KEYS_TYPES.keys())

    @staticmethod
    def database_keytypes():
        return COLLECTION_KEYS_TYPES

    @staticmethod
    def sql_create_table():
        return collection_sql

    @staticmethod
    def collection_type():
        return 'COLLECTION'

    @staticmethod
    def from_db_values(values):
        return Collection(values[2], values[1], values[0])

class Deck(Collection):
    def __init__(self, name, path, format='kitchen', unqkey=None, tablename='', type='DECK'):
        super().__init__(name, path, unqkey, tablename, type)
        self.format = format

    #def get_card_inserts(self):
        #return [(c.id, c.count, c.board) for c in self.cards]

    @staticmethod
    def from_db_values(values):
        return Deck(values[2], values[1], values[3], values[0])

    @staticmethod
    def database_keys():
        return tuple(DECK_KEYS_TYPES.keys())

    @staticmethod
    def database_keytypes():
        return DECK_KEYS_TYPES

    @staticmethod
    def sql_create_table():
        return deck_sql

    @staticmethod
    def collection_type():
        return 'DECK'

class _Base:
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, val):
        if not hasattr(self, key):
            raise KeyError('No key by name of '+key)
        setattr(self, key, val)

    def get_db_values(self, keytypes, primarykey):
        reStr = []
        keys = tuple(keytypes.keys())
        for k in keys:
            if self[k] is None:
                if k == 'id': reStr.append(self.create_id())
                if k == primarykey:
                    raise ValueError('Primary key is None')
                reStr.append(self[k])
            else:
                reStr.append(CONVERSION_TO_SQL[keytypes[k]](k, self[k]))
        return tuple(reStr)

    @staticmethod
    def from_db_values(reType, values, keytypes):
        keys = list(keytypes.keys())
        if len(keys) != len(values):
            raise ValueError('Keys and values must be of the same length')
        reSet = reType()
        cnt = 0
        while cnt < len(keys):
            if values[cnt] is None:
                reSet[keys[cnt]] = values[cnt]
            else:
                reSet[keys[cnt]] = CONVERSION_TO_Py[keytypes[keys[cnt]]](keys[cnt], values[cnt])
            cnt += 1
        return reSet


class Card(_Base):
    def __init__(self):
        self.__id = None
        self.multiverse_id = None
        self.collectors_number = None
        self.name = None
        self.set_code = None
        self.color = None
        self.mana_cost = None
        self.cmc = None
        self.rarity = None
        self.power = None
        self.toughness = None
        self.loyalty = None
        self.flavor_text = None
        self.type_line = None
        self.oracle_text = None
        self.artist = None
        self.layout = None
        self.types = None
        self.subtypes = None
        self.supertypes = None
        self.foreign_names = None
        self.rulings = None
        self.legalities = None
        self.image_url = None
        self.language = None
        self.card_face = None
        self.__count = 0
        self.board = 'M'
        self.extras = {}

    def collect_int(self):
        if not self.collectors_number:
            return float('inf')
        digs = []
        for c in self.collectors_number:
            if c.isdigit(): digs.append(c)
        num = ''.join(digs)
        if num:
            return int(''.join(digs))
        else:
            return float('inf')

    def get_db_values(self):
        return super().get_db_values(MTGCARDS_KEYS_TYPES, MTGCARDS_PRIMARY)

    def create_id(self):
        collect_num = ''
        multi_id = ''
        if self.multiverse_id is None and self.collectors_number is None:
            raise ValueError('Must contain at least a collectors_number or a multiverse_id ' + str(self.name) + ' ' + str(self.set_code)) #This Stops the loading from_db_values
            logging.debug('Failure to create id {} {} {} {}'.format(self.name, self.set_code, self.multiverse_id, self.collectors_number))
            #return self.__id
        if self.multiverse_id is not None:
            multi_id = str(self.multiverse_id)
        if self.collectors_number is not None:
            collect_num = str(self.collectors_number)
        return sha1((self.name + self.set_code + multi_id + collect_num).encode()).hexdigest()

    def _getId(self):
        return self.__id

    def _setId(self, newVal):
        self.__id = str(newVal)
    id = property(_getId, _setId)

    def _getCount(self):
        return self.__count

    def _setCount(self, cnt):
        if cnt is None or cnt == '':
            self.__count = 0
        else:
            self.__count = int(cnt)
    count = property(_getCount, _setCount)

    def __eq__(self, right):
        return self.id == right.id

    @staticmethod
    def from_db_values(values, keytypes=MTGCARDS_KEYS_TYPES): #Don't think this static keys types thing is going to work anymore. Once we throw a join in everything is going to go to hell
        card = _Base.from_db_values(Card, values, keytypes)
        if None == card.id:
            card.id = card.create_id()
        return card

    @staticmethod
    def from_MTG_SDK(card):
        reCard = Card()
        reCard.multiverse_id = card.multiverse_id
        reCard.collectors_number = card.number
        reCard.name = card.name
        reCard.set_code = card.set
        reCard.color = card.colors
        reCard.mana_cost = card.mana_cost
        reCard.cmc = card.cmc
        reCard.rarity = card.rarity
        reCard.power = card.power
        reCard.toughness = card.toughness
        reCard.loyalty = card.loyalty
        reCard.flavor_text = card.flavor
        reCard.type_line = card.type
        reCard.oracle_text = card.text
        reCard.artist = card.artist
        reCard.layout = card.layout
        reCard.types = card.types
        reCard.subtypes = card.subtypes
        reCard.supertypes = card.supertypes
        reCard.foreign_names = card.foreign_names
        reCard.rulings = card.rulings
        reCard.legalities = card.legalities
        reCard.image_url = card.image_url
        reCard.id = reCard.create_id()
        #reCard.language = card.language
        return reCard

    @staticmethod
    def from_scryfall(scrydict, skip_id=False):
        reCard = Card()
        reCard.multiverse_id = scrydict.get('multiverse_id', None)
        reCard.collectors_number = scrydict.get('collector_number', None)
        reCard.name = scrydict.get('name', None)
        reCard.set_code = scrydict.get('set', None)
        try:
            reCard.color = [SCRYFALL_COLORS[c] for c in scrydict['colors']]
        except KeyError:
            logging.error('ERROR ON ' + scrydict.get('name', '') + ' Set ' + scrydict.get('set', ''))
        reCard.mana_cost = scrydict.get('mana_cost', None)
        reCard.cmc = scrydict.get('cmc', None)
        reCard.rarity = scrydict.get('rarity', None)
        reCard.power = scrydict.get('power', None)
        reCard.toughness = scrydict.get('toughness', None)
        reCard.loyalty = scrydict.get('loyalty', None)
        reCard.flavor_text = scrydict.get('flavor_text', None)
        reCard.type_line = scrydict.get('type_line', None)
        reCard.oracle_text = scrydict.get('oracle_text', None)
        reCard.artist = scrydict.get('artist', None)
        reCard.layout = scrydict.get('layout', None)
        #reCard.types = scrydict.types #I'm hoping to create these from the type line property
        #reCard.subtypes = scrydict.subtypes
        #reCard.supertypes = scrydict.supertypes
        #reCard.foreign_names = None
        #reCard.rulings = scrydict.rulings
        reCard.legalities = scrydict.get('legalities', None)
        if 'image_uri' in scrydict:
            reCard.image_url = scrydict.get('image_uri', None)
        else:
            if 'image_uris' in scrydict:
                reCard.image_url = scrydict['image_uris'].get('normal', None)
        if not skip_id:
            reCard.id = reCard.create_id()
        #reCard.language = card.language
        return reCard

    @staticmethod
    def from_flip_scryfall(scrydict):
        if 'card_faces' not in scrydict:
            return [Card.from_scryfall(scrydict)]
        reCards = [Card.from_scryfall(scrydict['card_faces'][0], True), Card.from_scryfall(scrydict['card_faces'][1], True)]
        reCards[0].collectors_number = reCards[1].collectors_number = scrydict.get('collector_number', None)
        reCards[0].multiverse_id = scrydict['multiverse_ids'][0]
        reCards[1].multiverse_id = scrydict['multiverse_ids'][1]
        reCards[0].id = reCards[0].create_id()
        reCards[1].id = reCards[1].create_id()
        reCards[0].card_face = reCards[1].id
        reCards[1].card_face = reCards[0].id
        reCards[0].cmc = reCards[1].cmc = scrydict.get('cmc', None)
        reCards[0].layout = reCards[1].layout = scrydict.get('layout', None)
        reCards[0].legalities = reCards[1].legalities = scrydict.get('legalities', None)

class Set(_Base):
    def __init__(self):
        self.set_code = None
        self.name = None
        self.block = None
        self.border = None
        self.gatherer_code = None
        self.release_date = None
        self.booster = None
        self.online_only = None
        self.icon_svg_uri = None
        self.card_count = None
        self.set_type = None

    def get_db_values(self):
        return super().get_db_values(MTGSETS_KEYS_TYPES, MTGSETS_PRIMARY)

    @staticmethod
    def from_db_values(values):
        return _Base.from_db_values(Set, values, MTGSETS_KEYS_TYPES)

    @staticmethod
    def from_MTG_SDK(one_set):
        reSet = Set()
        reSet.code = one_set.code
        reSet.name = one_set.name
        reSet.block = one_set.block
        reSet.border = one_set.border
        reSet.gatherer_code = one_set.gatherer_code
        if one_set.release_date is None:
            reSet.release_date = None
        else:
            reSet.release_date = datetime.strptime(one_set.release_date, '%Y-%m-%d')
        reSet.booster = one_set.booster
        reSet.online_only = one_set.online_only
        return reSet

    @staticmethod
    def from_scryfall(values):
        reSet = Set()
        reSet.set_code = values['code']
        reSet.name = values['name']
        reSet.release_date = values.get('released_at', None)
        if reSet.release_date is not None:
            reSet.release_date = datetime.strptime(values['released_at'], '%Y-%m-%d')
        reSet.card_count = values['card_count']
        reSet.icon_svg_uri = values['icon_svg_uri']
        reSet.set_type = values.get('set_type', None)
        reSet.block = values.get('block', None)
        return reSet

def all_types():
    return ('DECK',
            'COLLECTION',
            'QUBE')

def get_class(type):
    if type.upper() == 'DECK':
        return Deck
    else:
        return Collection
if __name__ == '__main__':
    import mtgsdk
