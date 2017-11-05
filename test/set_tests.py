#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
from os.path import exists
from time import sleep
import json

import pytest

import mtgsdk
import inventories
from inventories import mtgdbhandler
from inventories.externalapis import mtgsdkreader
from inventories.externalapis import scryfalldealer
from inventories import Card
from utils.csvhandlers import tcgplayer_csv_to_cards
from utils import logsetup

store = None
DB_TEST_FILE = './test/test.mtg'

@pytest.mark.skip
def test_mtgsdk_conversion():
    mtgsdk_dict = {'code': 'UNH', 'name': 'Unhinged', 'type': 'un', 'border': 'silver', 'mkm_id': 59, 'mkm_name': 'Unhinged', 'release_date': '2004-11-20', 'gatherer_code': None, 'magic_cards_info_code': 'uh', 'booster': ['rare', 'uncommon', 'uncommon', 'uncommon', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'land'], 'old_code': None, 'block': None, 'online_only': None}
    s = mtgsdk.Set(mtgsdk_dict)
    assert inventories.Set.from_MTG_SDK(s).code == mtgsdk_dict['code']

def test_create_new():
    store = mtgdbhandler.MTGDatabaseHandler()
    store.create_new_db(DB_TEST_FILE)
    assert exists(DB_TEST_FILE)


@pytest.fixture
def store():
    store = mtgdbhandler.MTGDatabaseHandler()
    store.open_file(DB_TEST_FILE)
    return store

def test_has_tables(store):
    assert [mtgdbhandler.MTGSETS_TABLE_NAME, mtgdbhandler.MTGCARDS_TABLE_NAME, mtgdbhandler.MTG_USERBUILD_TABLE_NAME, 'sqlite_sequence'] == store.gettables()

def test_add_all_sets(store):
    all_sets = scryfalldealer.all_sets()
    assert 0 != len(all_sets)
    store.insert_sets(all_sets)

def test_find_set_exact(store):
    s = store.find_sets_exact(set_code='unh')
    assert len(s) == 1
    assert s[0].name == 'Unhinged'

def test_find_sets(store):
    s = store.find_sets_by_like(name='Un')
    assert len(s) == 11 #It's 11 due to the fact that the search is LIKE "%Un%"

def test_get_add_card(store):
    x = mtgsdk.Card.where(name='Shoe Tree').all()
    c = inventories.Card.from_MTG_SDK(x[0])
    assert '600df87fcdd54ae4c1fafdb32d9c695142d54a4c' == c.id
    #print(c.name, c.set_code, c.collectors_number, c.multiverse_id, c.id)


def test_insert_single_card(store):
    x = mtgsdk.Card.where(name='Shoe Tree').all()
    c = inventories.Card.from_MTG_SDK(x[0])
    store.insert_cards([c])

@pytest.mark.skip
def test_insert_many_cards(store):
    store.insert_cards([inventories.Card.from_MTG_SDK(c) for c in mtgsdk.Card.where(set_name='"Unglued"').all()])

def test_query_and_insert(store):
    store.find_cards_exact_to_external(name='Bad Ass')

def test_find_card(store):
    c = store.find_cards_exact(id='ffe01dd0fa385d6b0ced59e70d850619dff3c150')
    assert 'ffe01dd0fa385d6b0ced59e70d850619dff3c150' == c[0].id

def test_find_card_name(store):
    c = store.find_cards_exact(name='Shoe Tree')
    assert '600df87fcdd54ae4c1fafdb32d9c695142d54a4c' == c[0].id and c[0].name == 'Shoe Tree'

def test_add_collection(store):
    cols = store.create_collection('TESTER', 'here/there')
    assert 'TESTER' == cols.name
    assert 'here/there' == cols.path

#@pytest.mark.skip
def test_tcgplayer_csv_reads(store):
    cards = tcgplayer_csv_to_cards('/home/zac/Downloads/TCGplayerCardList (1).csv',  store.all_set_codes())
    suc, fails = store.find_cards_from_cards_external(cards)
    for f in fails:
        print('FAILED Name: ', f.name, ' Set Code: ', f.set_code)
    assert 0 == len(fails)
    store.create_deck('Pauper', 'decks/pauper', 'pauper', suc)

@pytest.mark.skip
def test_single_load():
    x = json.load(open('./test/support/single.json'))
    card = Card.from_scryfall(x)
    print(card.get_db_values())

@pytest.mark.skip
def test_scryfall():
    c = Card()
    c.name = "Bog Imp"
    cards = scryfalldealer.find_cards_by_name([c])
    print(cards)

@pytest.mark.skip
def get_a_set():
    import mtgsdk
    mtgsdk_dict = {'code': 'UNH', 'name': 'Unhinged', 'type': 'un', 'border': 'silver', 'mkm_id': 59, 'mkm_name': 'Unhinged', 'release_date': '2004-11-20', 'gatherer_code': None, 'magic_cards_info_code': 'uh', 'booster': ['rare', 'uncommon', 'uncommon', 'uncommon', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'land'], 'old_code': None, 'block': None, 'online_only': None}
    s = mtgsdk.Set(mtgsdk_dict)
    return Set.from_MTG_SDK(s)

if __name__ == '__main__':
    test_tcgplayer_csv_reads(store())
    #test_scryfall()
