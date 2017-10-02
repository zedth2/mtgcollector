#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
from os.path import dirname, abspath, sep

PROJECT_ROOT = abspath(dirname(__file__)) + sep

MEDIA_LOCATION = abspath(PROJECT_ROOT+'../media')

CARD_IMAGE_LOCATION = abspath(MEDIA_LOCATION+'/cardimgs')

DEFAULT_CARD_ICON = abspath(MEDIA_LOCATION + '/template.png')

URL_LENGTH = 300
