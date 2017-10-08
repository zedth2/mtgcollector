#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

import mtgsdk

from .. import Set, Card

SET_MAPPINGS_MTG_SDK = {'code' : 'code',
                        'name' : 'name',
                        'block' : 'block',
                        'border' : 'border',
                        'gatherer_code' : 'gatherer_code',
                        'release_date' : 'release_date',
                        'booster' : 'booster',
                        'online_only' : 'online_only'}

CARD_MAPPINGS_MTG_SDK ={'multiverse_id' : 'multiverse_id',
                        'collectors_number' : 'number',
                        'name' : 'name',
                        'set_code' : 'set',
                        'color' : 'colors',
                        'mana_cost' : 'mana_cost',
                        'cmc' : 'cmc',
                        'rarity' : 'rarity',
                        'power' : 'power',
                        'toughness' : 'toughness',
                        'loyalty' : 'loyalty',
                        'flavor_text' : 'flavor',
                        'type_line' : 'type',
                        'oracle_text' : 'text',
                        'artist' : 'artist',
                        'layout' : 'layout',
                        'types' : 'types',
                        'subtypes' : 'subtypes',
                        'supertypes' : 'supertypes',
                        'foreign_names' : 'foreign_names',
                        'rulings' : 'rulings',
                        'legalities' : 'legalities',
                        'image_url' : 'image_url'}
def convert_where(mappins, **kwargs):
    re = {}
    for k, v in kwargs.items():
        if k in mappins:
            re[mappins[k]] = v
        else:
            re[k] = v
    return re

def convert_set_where(**kwargs):
    return convert_where(SET_MAPPINGS_MTG_SDK, **kwargs)
def convert_card_where(**kwargs):
    return convert_where(CARD_MAPPINGS_MTG_SDK, **kwargs)

def mtgsdk_to_collector(items, collectorType):
    #if not isinstance(sets, (list, tuple)):
        #sets = [sets]
    reLst = []
    for s in items:
        reLst.append(collectorType.from_MTG_SDK(s))
    return reLst


def all_sets():
    return mtgsdk_to_collector(mtgsdk.Set.all(), Set)

def where_set(**kwargs):
    return mtgsdk_to_collector(mtgsdk.Set.where(**convert_set_where(**kwargs)).iter(), Set)

def where_card(**kwargs):
    return mtgsdk_to_collector(mtgsdk.Card.where(**convert_card_where(**kwargs)).iter(), Card)
