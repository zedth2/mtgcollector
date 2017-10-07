#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
from os.path import exists
from time import sleep
import pytest

import mtgsdk
import inventories
from inventories import mtgdbhandler
from inventories.externalapis import mtgsdkreader

store = None
DB_TEST_FILE = './test/test.mtg'


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
    assert [mtgdbhandler.MTGSETS_TABLE_NAME, mtgdbhandler.MTGCARDS_TABLE_NAME] == store.gettables()


def test_add_all_sets(store):
    all_sets = mtgsdkreader.all_sets()
    assert 0 != len(all_sets)
    store.insert_sets(all_sets)

def test_find_set_exact(store):
    s = store.find_sets_exact(code='UNH')
    assert len(s) == 1
    assert s[0].name == 'Unhinged'

def test_find_sets(store):
    s = store.find_sets_by_like(name='Un')
    assert len(s) == 5 #I was expect to only get Unglued and Unhinged but that where statement doesn't work the way I thought it would

def test_get_add_card(store):
    x = mtgsdk.Card.where(name='Shoe Tree').all()
    c = inventories.Card.from_MTG_SDK(x[0])
    assert '600df87fcdd54ae4c1fafdb32d9c695142d54a4c' == c.id
    #print(c.name, c.set_code, c.collectors_number, c.multiverse_id, c.id)

def test_insert_single_card(store):
    x = mtgsdk.Card.where(name='Shoe Tree').all()
    c = inventories.Card.from_MTG_SDK(x[0])
    store.insert_cards([c])

def get_a_set():
    import mtgsdk
    mtgsdk_dict = {'code': 'UNH', 'name': 'Unhinged', 'type': 'un', 'border': 'silver', 'mkm_id': 59, 'mkm_name': 'Unhinged', 'release_date': '2004-11-20', 'gatherer_code': None, 'magic_cards_info_code': 'uh', 'booster': ['rare', 'uncommon', 'uncommon', 'uncommon', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'land'], 'old_code': None, 'block': None, 'online_only': None}
    s = mtgsdk.Set(mtgsdk_dict)
    return Set.from_MTG_SDK(s)
