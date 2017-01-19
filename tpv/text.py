# -*- coding: utf-8 -*-
"""Programa tpv para la pizeria Btres

    Autor: Manuel Rodriguez
    Licencia: Apache v2.0

"""
from kivy.storage.jsonstore import JsonStore
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)



if __name__ == '__main__':
    db = JsonStore("db/menupizza.json")
    print db
