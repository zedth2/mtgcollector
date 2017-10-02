#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

from mtgsdk import Card


class CardItem(Card):
    def __init__(self, response_dict={}):
        super().__init__(response_dict)
        self.quantity = response_dict.get('quantity', 1)
