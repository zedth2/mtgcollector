#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
import json

from urllib.parse import quote
from urllib import request
from .. import Set, Card
SCRYFALL_URL = 'https://api.scryfall.com/'
SCRYFALL_CARD_SEARCH = SCRYFALL_URL + 'cards/search?'


def find_cards_by_name(cards):
    query = 'q='
    names = []
    for c in cards:
        if c.name is not None:
            names.append('"' + c.name + '"')
    query = 'q=' + quote(' or '.join(names))
    return parse_response(query_scryfall(SCRYFALL_CARD_SEARCH + query))

def query_scryfall(url):
    return json.loads(request.urlopen(url).read().decode())

def parse_response(response):
    cards = []
    for c in response['data']:
        cards.append(Card.from_scryfall(c))
    return cards
