#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
from os.path import exists
from time import sleep
import unittest
import mtgsdk
import inventories
from inventories import mtgdbhandler
from inventories.externalapis import mtgsdkreader

DB_TEST_FILE = './test/test.mtg'
class TestSets(unittest.TestCase):

    def test_mtgsdk_conversion(self):
        mtgsdk_dict = {'code': 'UNH', 'name': 'Unhinged', 'type': 'un', 'border': 'silver', 'mkm_id': 59, 'mkm_name': 'Unhinged', 'release_date': '2004-11-20', 'gatherer_code': None, 'magic_cards_info_code': 'uh', 'booster': ['rare', 'uncommon', 'uncommon', 'uncommon', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'land'], 'old_code': None, 'block': None, 'online_only': None}
        s = mtgsdk.Set(mtgsdk_dict)
        self.assertEqual(inventories.Set.from_MTG_SDK(s).code, mtgsdk_dict['code'])

    def test_create_new(self):
        store = mtgdbhandler.MTGDatabaseHandler()
        store.create_new_db(DB_TEST_FILE)
        tables = store.gettables()
        self.assertTrue(exists(DB_TEST_FILE))
        self.assertEqual([mtgdbhandler.MTGSETS_TABLE_NAME], tables)
        store.openDB.close()

    def test_has_tables(self):
        store = mtgdbhandler.MTGDatabaseHandler()
        store.open_file(DB_TEST_FILE)
        tables = store.gettables()
        self.assertEqual([mtgdbhandler.MTGSETS_TABLE_NAME], tables)
        store.openDB.close()

    def test_add_all_sets(self):
        sleep(1)
        store = mtgdbhandler.MTGDatabaseHandler()
        store.open_file(DB_TEST_FILE)
        all_sets = mtgsdkreader.all_sets()

        self.assertNotEqual(0, len(all_sets))
        store.insert_sets(all_sets)


if __name__ == '__main__':
    unittest.main()
