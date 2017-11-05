#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
import sys
import logging
logformat = '%(asctime)s - %(filename)s %(funcName)s - %(levelname)s'
logging.basicConfig(format=logformat)
root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
root.addHandler(ch)
