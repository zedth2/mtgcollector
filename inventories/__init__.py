#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
from hashlib import sha1
from datetime import datetime
from .sqlments import MTGSETS_KEYS_TYPES, MTGSETS_PRIMARY, MTGCARDS_KEYS_TYPES, CONVERSION_TO_Py, CONVERSION_TO_SQL, MTGCARDS_PRIMARY
import json

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
        #self.id = None
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

    def get_db_values(self):
        return super().get_db_values(MTGCARDS_KEYS_TYPES, MTGCARDS_PRIMARY)

    @property
    def id(self):
        if self.multiverse_id is None and self.number is None:
            raise ValueError('Must contain at least a number or a multiverse_id')
        return sha1((self.name + self.set_code + str(self.multiverse_id) + str(self.collectors_number)).encode()).hexdigest()

    @staticmethod
    def from_db_values(values):
        return _Base.from_db_values(Card, values, MTGCARDS_KEYS_TYPES)

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
