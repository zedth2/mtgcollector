#!/usr/bin/python3

def dicttotable(obj, tablename):
    reStr = 'CREATE TABLE '+tablename+' ('
    for k, v in obj.__dict__.items():
        reStr += str(k) + ' ' + typefind(v) + ', --Orginal Type ' + str(type(v)) + '\n'
    return reStr



def typefind(origType):
    reStr = 'TEXT'
    if isinstance(origType, int):
        reStr = 'INTEGER'
    elif isinstance(origType, float):
        reStr = 'REAL'
    elif isinstance(origType, (tuple, list, dict)):
        reStr = 'TEXT'
    elif origType is None:
        reStr = "ERROR"
    return reStr

from mtgsdk import Card
c = Card.where(types='creature').where(subtypes='elf').where(colors='black').all()
print(dicttotable(c[0], 'mtgcards'))
