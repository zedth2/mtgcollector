#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

from datetime import datetime
from .mtgdbhandler import MTGSETS_KEYS
class Card:
    def __init__(self):
        self.id = None
        self.multiverse_id = None
        self.collectors_number = None
        self.name = None
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

    def __getitem__(self, key):
        return getattr(self, key)

    @staticmethod
    def from_db_values(self, keys, values):
        pass

    @staticmethod
    def from_MTG_SDK(card):
        self.multiverse_id = card.multiverse_id
        self.collectors_number = card.number
        self.name = card.name
        self.color = card.colors
        self.mana_cost = card.mana_cost
        self.cmc = card.cmc
        self.rarity = card.rarity
        self.power = card.power
        self.toughness = card.toughness
        self.loyalty = card.loyalty
        self.flavor_text = card.flavor
        self.type_line = card.type
        self.oracle_text = card.text
        self.artist = card.artist
        self.layout = card.layout
        self.types = card.types
        self.subtypes = card.subtypes
        self.supertypes = card.supertypes
        self.foreign_names = card.foreign_names
        self.rulings = card.rulings
        self.legalities = card.legalities
        self.image_url = card.image_url
        self.language = card.language


class Set:
    def __init__(self):
        self.code = None
        self.name = None
        self.block = None
        self.border = None
        self.gatherer_code = None
        self.release_date = None
        self.booster = None

    def get_db_values(self, keys=MTGSETS_KEYS):
        reStr = []
        for k in keys:
            if self[k] is None:
                reStr.append(self[k])
            if k in ('code', 'name', 'block', 'border', 'gatherer_code'):
                reStr.append(str(self[k]))
            elif k in ('release_date',):
                if isinstance(self[k], datetime):
                    reStr.append(self[k].timestamp())
            elif k in ('booster',):
                reStr.append(','.join(self[k]))
            else: #I think the first if will take care of this
                raise ValueError('Failure to find key ' + k)
        return tuple(reStr)

    def __getitem__(self, key):
        return getattr(self, key)

    @staticmethod
    def from_db_values(self, values, keys=MTGSETS_KEYS):
        if len(keys) != len(values):
            raise ValueError('Keys and values must be of the same length')
        reSet = Set()
        cnt = 0
        while cnt < len(k):
            if values[cnt] is None:
                reSet[keys[cnt]] = values[cnt]
            if keys[cnt] in ('code', 'name', 'block', 'border', 'gatherer_code'):
                reSet[keys[cnt]] = str(values[cnt])
            elif keys[cnt] in ('release_date',):
                reSet[keys[cnt]] = datetime.fromtimestamp(values[cnt])
            elif keys[cnt] in ('booster',):
                reSet[keys[cnt]] = values[cnt].split(',')
            else: #I think the first if will take care of this
                raise ValueError('Failure to find key ' + k)
        return reSet

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
