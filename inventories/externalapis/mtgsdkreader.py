#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

import mtgsdk

from .. import Set

def mtgsdk_to_collector(sets):
    #if not isinstance(sets, (list, tuple)):
        #sets = [sets]
    reLst = []
    for s in sets:
        reLst.append(Set.from_MTG_SDK(s))
    return reLst


def all_sets():
    return mtgsdk_to_collector(mtgsdk.Set.all())

def where_set(**kwargs):
    return mtgsdk_to_collector(mtgsdk.Set.where(**kwargs).iter())
