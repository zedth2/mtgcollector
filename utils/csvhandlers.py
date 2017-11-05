#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
import logging
import csv
from inventories import Card

TCGPLAYER_MAPPINGS = {  'Quantity':'count',
                        'Name' : 'name',
                        #'Set' : None, #The full name of the set which we should already have
                        'Card Number' : 'collectors_number',
                        'Set Code' : 'set_code',
                        #'Variant' : 'None', #I'm assuming this marks it as foil or whatever which we should probably add into our card type
                        #'Condition' : None, #I don't think we card about this
                        'Language' : 'language',
                        'Rarity' : 'rarity',
                        #'Product ID' : None #I'm assuming this is their product id so fuck it
                        #'SKU' : None, #Same as above
                     }

SET_CODE_MAPPINGS = {'7E' : '7ed',
                     '6E' : '6ed',
                     '8E' : '8ed',
                     '9E' : '9ed',
                     'PR' : 'pcy',
                     'MI' : 'mir',
                     'UZ' : 'usg',
                     'LE' : 'leg',
                     'CSP2' : 'cst',
                     'EX' : 'exo',
                     'IN' : 'inv',
                     'CG' : 'uds',
                     'GU' : 'ulg',
                     'UZ' : 'usg'}

def tcgplayer_csv_to_cards(csvFile, avaiableSets=[]):
    reLst = {}
    with open(csvFile) as f:
        dcsv = csv.DictReader(f)
        for c in dcsv:
            card = tcgplayer_dict_to_card(c, avaiableSets)
            if card.name:
                #print('NAME ', card.name, ' COUNT ', card.count)
                if card.name in reLst:
                    if reLst[card.name].set_code == card.set_code:
                        reLst[card.name].count += 1
                else:
                    reLst[card.name] = card
            else:
                try:
                    reLst['UNKNOWNS'].append(card)
                except KeyError:
                    reLst['UNKNOWNS'] = [card]
    return tuple(reLst.values())

def tcgplayer_dict_to_card(cardict, avaiableSets=[]):
    reCard = Card()
    for k, v in cardict.items():
        try:
            val = v
            if k == 'Set Code':
                val = v.lower()
                if val not in avaiableSets:
                    logging.debug('CHANGING UP from ' + val + ' to ' + SET_CODE_MAPPINGS.get(v, 'None'))
                    val = SET_CODE_MAPPINGS.get(v, None)
            local = TCGPLAYER_MAPPINGS[k]
            reCard[local] = val
        except KeyError:
            pass

    return reCard


if __name__ == '__main__':
    tcgplayer_csv_to_cards('./test/pauper.csv')
