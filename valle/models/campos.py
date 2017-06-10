# -*- coding: utf-8 -*-

"""Programa Gestion para el TPV del Btres

    Autor: Manuel Rodriguez
    Licencia: Apache v2.0

"""

class Campo(object):
    dato = None
    tipo = "TEXT"
    def __init__(self, **kargs):
        if "dato" in kargs:
            self.dato = kargs["dato"]
        if "tipo" in kargs:
            self.tipo = kargs["tipo"]
        
    def __set_dato__(self):
        tipo = type(self.tipo)
        if tipo is int:
            self.tipo = "INTEGER"
        if tipo is float:
            self.tipo = "REAL"
        else:
            self.tipo = "TEXT"


    def pack(self):
        self.__set_dato__()
        if self.tipo is "TEXT":
            return '"{0}"'.format(unicode(self.dato))
        else:
            return self.dato

    def getTipoDatos(self):
        self.__set_dato__()
        return self.tipo

    def get(self):
        self.__set_dato__()
        return self.dato

    def set(self, val):
        self.dato = val
        self.__set_dato__()
