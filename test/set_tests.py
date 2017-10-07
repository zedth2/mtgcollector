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
    #tables = self.store.gettables()
    assert exists(DB_TEST_FILE)

    #self.store.openDB.close()


@pytest.fixture
def store():
    store = mtgdbhandler.MTGDatabaseHandler()
    store.open_file(DB_TEST_FILE)
    return store

def test_has_tables(store):
    #self.store = mtgdbhandler.MTGDatabaseHandler()
    #self.store.open_file(DB_TEST_FILE)
    assert [mtgdbhandler.MTGSETS_TABLE_NAME] == store.gettables()
    #self.store.openDB.close()

def test_add_all_sets(store):
    #store = mtgdbhandler.MTGDatabaseHandler()
    #store.open_file(DB_TEST_FILE)
    #print('test_add_all_sets', store)
    #print(DB_TEST_FILE, store.gettables())
    all_sets = mtgsdkreader.all_sets()

    assert 0 != len(all_sets)

    store.insert_sets(all_sets)

#set_tester = SetTest()

#def test_mtgsdk_conversion(self):
#set_tester.test_mtgsdk_conversion()

#def test_create_new(self):
#set_tester.test_create_new()

#def test_has_tables(self):
#set_tester.test_has_tables()

#def test_add_all_sets(self):
#set_tester.test_add_all_sets()

def get_a_set():
    import mtgsdk
    mtgsdk_dict = {'code': 'UNH', 'name': 'Unhinged', 'type': 'un', 'border': 'silver', 'mkm_id': 59, 'mkm_name': 'Unhinged', 'release_date': '2004-11-20', 'gatherer_code': None, 'magic_cards_info_code': 'uh', 'booster': ['rare', 'uncommon', 'uncommon', 'uncommon', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'land'], 'old_code': None, 'block': None, 'online_only': None}
    s = mtgsdk.Set(mtgsdk_dict)
    return Set.from_MTG_SDK(s)



#if __name__ == '__main__':
    ##unittest.main()
    #test_insert_all_sets()
    #store.close_db_no_error()
