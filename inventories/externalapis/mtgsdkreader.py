#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

import mtgsdk
from mtgsdk import config
from utils.config import URL_LENGTH
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

def find_many_cards(cards):
    '''
    This will query mtgsdk looking for cards by name. Every card must have a name or a ValueError is raised.
    '''
    finds = []
    names = []
    query_str = ''
    urllen = len(config.__endpoint__ + mtgsdk.Card.RESOURCE)
    curlen = urllen + len('name=') + 2
    for c in cards:
        if c.name is None or c.name == '':
            raise ValueError('Card does not contain a name to query for')
        #curlen += len(c.name) + 1 #The place one is for the `|` that will be put in.
        if (curlen+len(c.name)+1) < URL_LENGTH:
            curlen += len(c.name)+1
            names.append(c.name)
        else:
            finds += where_card_or(name=names)
            names = []
            curlen = urllen + len('name=') + 2
    if len(names):
        finds += where_card_or(name=names)
    return finds

def where_card_or(**kwargs):
    wheres = {}
    finds = []
    for k, v in kwargs.items():
        wheres[k] = '|'.join(v)
    for m in mtgsdk.Card.where(**wheres).iter():
        finds.append(Card.from_MTG_SDK(m))
    return finds
