#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

import unittest
import mtgsdk
import inventories
from inventories import mtgdbhandler
from os.path import exists

class TestSets(unittest.TestCase):
    def test_mtgsdk_conversion(self):
        mtgsdk_dict = {'code': 'UNH', 'name': 'Unhinged', 'type': 'un', 'border': 'silver', 'mkm_id': 59, 'mkm_name': 'Unhinged', 'release_date': '2004-11-20', 'gatherer_code': None, 'magic_cards_info_code': 'uh', 'booster': ['rare', 'uncommon', 'uncommon', 'uncommon', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'common', 'land'], 'old_code': None, 'block': None, 'online_only': None}
        s = mtgsdk.Set(mtgsdk_dict)
        self.assertEqual(inventories.Set.from_MTG_SDK(s).code, mtgsdk_dict['code'])

    def test_create_new(self):
        store = mtgdbhandler.MTGDatabaseHandler()
        store.create_new_db('./test.mtg')
        tables = store.gettables()
        self.assertTrue(exists('./test.mtg'))
        self.assertEqual([mtgdbhandler.MTGSETS_TABLE_NAME], tables)

    def test_add_all_sets(self):
        pass


if __name__ == '__main__':
    unittest.main()
