#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
import logging
import imghdr
from os.path import exists
from glob import glob
from urllib import request
from PyQt5 import QtCore, QtGui, QtWidgets
from . import config


filemaps = {
    "{T}": "icons/tap.gif",
    "{Q}": "icons/untap.gif",
    "{U}": "icons/mana/Symbol_U_mana.gif",
    "{W}": "icons/mana/Symbol_W_mana.gif",
    "{B}": "icons/mana/Symbol_B_mana.gif",
    "{G}": "icons/mana/Symbol_G_mana.gif",
    "{R}": "icons/mana/Symbol_R_mana.gif",
    "{C}": "icons/mana/Symbol_C_mana.png",
    "{S}": "icons/mana/Symbol_snow_mana.gif",
    "{X}": "icons/mana/Symbol_X_mana.gif",
    "{Y}": "icons/mana/Symbol_Y_mana.gif",
    "{Z}": "icons/mana/Symbol_Z_mana.gif",
    "{0.5}": "icons/mana/Symbol_500_mana.gif",
    "{05}": "icons/mana/Symbol_500_mana.gif",
    "{500}": "icons/mana/Symbol_500_mana.gif",
    "{R/W}": "icons/mana/Symbol_RW_mana.gif",
    "{R/G}": "icons/mana/Symbol_RG_mana.gif",
    "{B/R}": "icons/mana/Symbol_BR_mana.gif",
    "{B/G}": "icons/mana/Symbol_BG_mana.gif",
    "{G/U}": "icons/mana/Symbol_GU_mana.gif",
    "{G/W}": "icons/mana/Symbol_GW_mana.gif",
    "{W/U}": "icons/mana/Symbol_WU_mana.gif",
    "{W/B}": "icons/mana/Symbol_WB_mana.gif",
    "{U/B}": "icons/mana/Symbol_UB_mana.gif",
    "{U/R}": "icons/mana/Symbol_UR_mana.gif",
    "{0}": "icons/mana/Symbol_0_mana.gif",
    "{1}": "icons/mana/Symbol_1_mana.gif",
    "{2}": "icons/mana/Symbol_2_mana.gif",
    "{3}": "icons/mana/Symbol_3_mana.gif",
    "{4}": "icons/mana/Symbol_4_mana.gif",
    "{5}": "icons/mana/Symbol_5_mana.gif",
    "{6}": "icons/mana/Symbol_6_mana.gif",
    "{7}": "icons/mana/Symbol_7_mana.gif",
    "{8}": "icons/mana/Symbol_8_mana.gif",
    "{9}": "icons/mana/Symbol_9_mana.gif",
    "{10}": "icons/mana/Symbol_10_mana.gif",
    "{11}": "icons/mana/Symbol_11_mana.gif",
    "{12}": "icons/mana/Symbol_12_mana.gif",
    "{14}": "icons/mana/Symbol_14_mana.gif",
    "{13}": "icons/mana/Symbol_13_mana.gif",
    "{15}": "icons/mana/Symbol_15_mana.gif",
    "{16}": "icons/mana/Symbol_16_mana.gif",
    "{1000000}": "icons/mana/Symbol_1000000_mana.gif",
    "{2/W}": "icons/mana/Symbol_2W_mana.gif",
    "{2/U}": "icons/mana/Symbol_2U_mana.gif",
    "{2/B}": "icons/mana/Symbol_2B_mana.gif",
    "{2/G}": "icons/mana/Symbol_2G_mana.gif",
    "{2/R}": "icons/mana/Symbol_2R_mana.gif",
    "{UP}": "icons/mana/Symbol_UP_mana.gif",
    "{WP}": "icons/mana/Symbol_WP_mana.gif",
    "{BP}": "icons/mana/Symbol_BP_mana.gif",
    "{GP}": "icons/mana/Symbol_GP_mana.gif",
    "{RP}": "icons/mana/Symbol_RP_mana.gif",
    }

def manaconversion(mana_cost, id=''):
    manas = mana_cost.split('}')
    width = height = 0
    prev = QtGui.QPixmap(filemaps['{B}'])
    height = prev.height()
    width = prev.width()
    paint = QtGui.QPainter()#QtGui.QPixmap(15*(len(manas)-1), 15))
    paint.drawPixmap(0,0, prev)

    #if len(manas) > 1:
        #cur = QtGui.QPixmap(filemaps['{B}'])
        #paint.drawPixmap(15,0, cur)
    #for m in manas[1:]:
        #if m != '':
            #cur = QtGui.QPixmap(filemaps[manas[0]+'}'])
            #paint.drawPixmap(width, 0, cur)
            #width += cur.width()
    icon = QtGui.QIcon()
    fin = QtGui.QPixmap(width, height)#15*(len(manas)-1), 15)
    icon.addPixmap(fin)
    fin.save(config.CARD_IMAGE_LOCATION+'/'+id+'.jpg', 'jpg')
    del paint
    return icon

def downloadimg(card):
    path = config.CARD_IMAGE_LOCATION + '/' + card.id

    files = glob(path + '*')
    if len(files) and exists(files[0]):
        logging.info('Local icon found: ' + files[0])
        return files[0]
    else:
        if card.image_url is None:
            logging.error('ERROR : No Icon for ' + card.name + ' ' + card.id)
            return config.DEFAULT_CARD_ICON
        logging.info('Downloading image from ' + card.image_url)
        bits = request.urlopen(card.image_url).read()
        ext = '.'+imghdr.what(None, bits)
        if ext is None:
            ext = '.jpg'
        with open(path + ext, 'wb') as f:
            f.write(bits)
    return path + ext
