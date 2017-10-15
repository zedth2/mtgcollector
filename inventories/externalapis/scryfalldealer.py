#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
import json

from urllib.parse import quote
from urllib import request
from inventories import Set, Card
SCRYFALL_URL = 'https://api.scryfall.com/'
SCRYFALL_CARD_SEARCH = SCRYFALL_URL + 'cards/search?'


def all_sets():
    return parse_response(query_scryfall(SCRYFALL_URL+'sets'), Set)

def find_cards_by_name(cards):
    query = 'q='
    names = []
    for c in cards:
        if c.name is not None:
            names.append('"' + c.name + '"')
    query = 'q=' + quote('++'+' or '.join(names))
    #print(query)
    return parse_response(query_scryfall(SCRYFALL_CARD_SEARCH + query), Card)

def query_scryfall(url):
    return json.loads(request.urlopen(url).read().decode())

def parse_response(response, localtype):
    cards = []
    for c in response['data']:
        cards.append(localtype.from_scryfall(c))
    if response['has_more']:
        cards += parse_response(query_scryfall(response['next_page']), localtype)
    print('Found this many cards ', len(cards))
    return cards


if __name__ == '__main__':
    for s in find_all_sets():
        print(s.name)
