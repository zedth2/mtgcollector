#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
import json
import logging
from urllib.parse import quote
from urllib import request
from inventories import Set, Card
SCRYFALL_URL = 'https://api.scryfall.com/'
SCRYFALL_CARD_SEARCH = SCRYFALL_URL + 'cards/search?'


def all_sets():
    return parse_response(query_scryfall(SCRYFALL_URL+'sets'), Set)

def find_cards_by_name(cards):
    query = 'q='
    found = []
    name = ''
    for c in cards:
        if c.name is not None:
            cur = '++!"' + c.name + '"'
            if 500 <= (len(name) + 4 + len(cur)):
                found += parse_response(query_scryfall(SCRYFALL_CARD_SEARCH + 'q=' + quote(name)), Card)
                name = cur
            else:
                name = ' or '.join([name, '++!"' + c.name + '"'])
    if name:
        found += parse_response(query_scryfall(SCRYFALL_CARD_SEARCH + 'q=' + quote(name)), Card)
    return found

def find_cards_by_set(sets):
    if not isinstance(sets, (tuple, list)):
        sets = [sets]
    query = 'q='
    names = []
    for s in sets:
        names.append('++e:'+s.set_code)
    query += quote(' or '.join(names))
    return parse_response(query_scryfall(SCRYFALL_CARD_SEARCH + query), Card)

def query_scryfall(url):
    logging.info('Querying Scryfall ' + url)
    return json.loads(request.urlopen(url).read().decode())

def parse_response(response, localtype):
    cards = []
    for c in response['data']:
        if issubclass(localtype, Card):
            cards += parse_card_response(c)
        else:
            cards.append(localtype.from_scryfall(c))
    if response['has_more']:
        cards += parse_response(query_scryfall(response['next_page']), localtype)
    print('Found this many cards ', len(cards))
    return cards

def parse_card_response(scrycard):
    if scrycard['layout'] in ['normal', 'leveler', 'planar', 'scheme', 'token', 'emblem']:
        return [Card.from_scryfall(scrycard)]
    elif 'split' == scrycard['layout']:
        return from_card_split(scrycard)
    elif 'transform' == scrycard['layout']:
        return from_card_transform(scrycard)
    elif 'flip' == scrycard['layout']:
        return from_card_flip(scrycard)
    elif 'meld' == scrycard['layout']:
        return from_card_meld(scrycard)
    elif 'vanguard' == scrycard['layout']:
        return from_card_vanguard(scrycard)
    else:
        raise ValueError('Do not know of type ' + scrycard.get('layout', 'NONE'))

def from_card_meld(scrydict):
    return [Card.from_scryfall(scrydict)]

def from_card_vanguard(scrydict):
    card = Card.from_scryfall(scrydict)
    card.extras.update({'life_modifier':scrydict['life_modifier'],
                        'hand_modifier':scrydict['hand_modifier']})
    return [card]

def from_card_transform(scrydict):
    one = Card.from_scryfall(scrydict['card_faces'][0], True)
    two = Card.from_scryfall(scrydict['card_faces'][1], True)
    if len(scrydict['multiverse_ids']):
        one.multiverse_id = scrydict['multiverse_ids'][0]
        try:
            two.multiverse_id = scrydict['multiverse_ids'][1]
        except IndexError:
            two.multiverse_id = scrydict['multiverse_ids'][0]
    else:
        id = None
        if 'multiverse_id' in scrydict:
            id = scrydict['multiverse_id']
        one.multiverse_id = two.multiverse_id = id
    one.set_code = two.set_code = scrydict.get('set', None)
    one.rarity = two.rarity = scrydict.get('rarity', None)
    one.artist = two.artist = scrydict.get('artist', None)
    one.layout = two.layout = scrydict.get('layout', None)
    one.cmc = two.cmc = scrydict.get('cmc', None)
    one.legalities = two.legalities = scrydict.get('legalities', None)
    one.collectors_number = two.collectors_number = scrydict.get('collector_number', None)
    one.id = two.card_face = one.create_id()
    two.id = one.card_face = two.create_id()
    return [one, two]

def from_card_flip(scrydict):
    card = Card.from_scryfall(scrydict)
    card.extras.update({'card_faces': scrydict['card_faces']})
    return [card]

def from_card_meld(scrydict):
    card = Card.from_scryfall(scrydict)
    card.extras.update({'all_parts': scrydict['all_parts']})
    return [card]

def from_card_split(scrydict):
    one = Card.from_scryfall(scrydict, True)
    two = Card.from_scryfall(scrydict, True)
    one.name = scrydict['card_faces'][0]['name']
    one.oracle_text = scrydict['card_faces'][0].get('oracle_text', None)
    one.type_line = scrydict['card_faces'][0].get('type_line', None)
    one.mana_cost = scrydict['card_faces'][0].get('mana_cost', None)
    if 'image_uris' in scrydict['card_faces'][0]:
        one.image_url = two.image_url = scrydict['card_faces'][0].get('image_uris', None)
    elif 'image_uris' in scrydict:
        one.image_url = two.image_url = scrydict['image_uris'].get('normal', None)
    one.toughness = scrydict['card_faces'][0].get('toughness', None)
    one.power = scrydict['card_faces'][0].get('power', None)
    two.toughness = scrydict['card_faces'][1].get('toughness', None)
    two.power = scrydict['card_faces'][1].get('power', None)
    two.cmc = one.cmc = scrydict['cmc']
    two.name = scrydict['card_faces'][1]['name']
    two.oracle_text = scrydict['card_faces'][1].get('oracle_text', None)
    two.type_line = scrydict['card_faces'][1].get('type_line', None)
    two.mana_cost = scrydict['card_faces'][1].get('mana_cost', None)
    one.id = one.create_id()
    two.id = two.create_id()
    one.card_face = two.id
    two.card_face = one.id
    return [one, two]

if __name__ == '__main__':
    for s in all_sets():
        print(s.name)
