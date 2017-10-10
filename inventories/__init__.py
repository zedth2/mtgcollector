#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
from hashlib import sha1
from datetime import datetime
from .sqlments import MTGSETS_KEYS_TYPES, MTGSETS_PRIMARY, MTGCARDS_KEYS_TYPES, CONVERSION_TO_Py, CONVERSION_TO_SQL, MTGCARDS_PRIMARY
import json

SCRYFALL_COLORS = {'U':'Blue','B':'Black', 'G':'Green', 'W':'White', 'R':'Red'}
class Collection:
    def __init__(self, name, path, unqkey=None):
        self.name = name
        self.path = path
        self.cards = []

    @property
    def unqkey(self):
        return self.__unqkey

    @staticmethod
    def from_db_values(values):
        return Collection(values[2], values[1], values[0])

class Deck(Collection):
    def __init__(self, name, path, format='kitchen', unqkey=None):
        super().__init__(name, path, unqkey)
        self.format = format

    @staticmethod
    def from_db_values(values):
        return Deck(values[2], values[1], values[3], values[0])

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
        self.count = 0

    def get_db_values(self):
        return super().get_db_values(MTGCARDS_KEYS_TYPES, MTGCARDS_PRIMARY)

    def create_id(self):
        collect_num = ''
        multi_id = ''
        if self.multiverse_id is None and self.collectors_number is None:
            raise ValueError('Must contain at least a collectors_number or a multiverse_id ' + str(self.name) + ' ' + str(self.set_code)) #This Stops the loading from_db_values
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

    @staticmethod
    def from_db_values(values):
        card = _Base.from_db_values(Card, values, MTGCARDS_KEYS_TYPES)
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
    def from_scryfall(scrydict):
        reCard = Card()
        reCard.multiverse_id = scrydict.get('multiverse_id', None)
        reCard.collectors_number = scrydict.get('collector_number', None)
        reCard.name = scrydict.get('name', None)
        reCard.set_code = scrydict.get('set', None)
        reCard.color = [SCRYFALL_COLORS[c] for c in scrydict['colors']]
        reCard.mana_cost = scrydict.get('mana_cost', None)
        reCard.cmc = scrydict['cmc']
        reCard.rarity = scrydict['rarity']
        reCard.power = scrydict['power']
        reCard.toughness = scrydict['toughness']
        reCard.loyalty = scrydict.get('loyalty', None)
        reCard.flavor_text = scrydict['flavor_text']
        reCard.type_line = scrydict['type_line']
        reCard.oracle_text = scrydict['oracle_text']
        reCard.artist = scrydict['artist']
        reCard.layout = scrydict['layout']
        #reCard.types = scrydict.types #I'm hoping to create these from the type line property
        #reCard.subtypes = scrydict.subtypes
        #reCard.supertypes = scrydict.supertypes
        #reCard.foreign_names = None
        #reCard.rulings = scrydict.rulings
        reCard.legalities = scrydict['legalities']
        reCard.image_url = scrydict['image_uri']
        reCard.id = reCard.create_id()
        #reCard.language = card.language
        return reCard

class Set(_Base):
    def __init__(self):
        self.code = None
        self.name = None
        self.block = None
        self.border = None
        self.gatherer_code = None
        self.release_date = None
        self.booster = None
        self.online_only = None

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


if __name__ == '__main__':
    import mtgsdk
