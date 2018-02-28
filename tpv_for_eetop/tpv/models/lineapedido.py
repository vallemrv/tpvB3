# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   04-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 15-Sep-2017
# @License: Apache license vesion 2.0



from kivy.event import EventDispatcher
from kivy.properties import (StringProperty, ObjectProperty,
                             ListProperty, BooleanProperty)

from valle_libs.utils import parse_float

class Linea(EventDispatcher):

    def __init__(self, obj, pun=0):
        self.puntero = pun
        self.obj = obj
        self.promocion = None

    def get_pregunta(self):
        db = None
        num = len(self.obj.get("preguntas"))
        if self.puntero < num:
            nombre = self.obj.get('preguntas')[self.puntero]
            db = "../db/preguntas/%s.json" % nombre
            self.puntero = self.puntero + 1
        return db

    def hay_preguntas(self):
        num = len(self.obj.get("preguntas"))
        return self.puntero < num

    def add_modificador(self, obj):
        self.obj['modificadores'].append(obj)

    def remove_modificador(self):
        if len(self.obj['modificadores']) > 0:
            self.obj['modificadores'].pop()

    def getPrecio(self):
        total = parse_float(self.obj.get('precio'))
        num_mod =len(self.obj.get('modificadores')) if "modificadores" in self.obj else 0
        for i in range(num_mod):
            mod = self.obj['modificadores'][i]
            total = total + self._getPrecioMod(mod)
        if self.promocion is not None:
            total *= float(self.promocion)
        return total

    def getTotal(self):
        total = parse_float(self.obj.get('precio'))
        num_mod =len(self.obj.get('modificadores')) if "modificadores" in self.obj else 0
        for i in range(num_mod):
            mod = self.obj['modificadores'][i]
            total = total + self._getPrecioMod(mod)
        total = total * self.obj['cant']
        if self.promocion is not None:
            total *= float(self.promocion)
        return total

    def _getPrecioMod(self, mod):
        total = parse_float(mod.get('precio'))
        num_mod =len(mod.get('modificadores')) if "modificadores" in mod else 0
        for i in range(num_mod):
            aux = mod['modificadores'][i]
            total = total + self._getPrecioMod(aux)
        return total

    def getTexto(self):
        texto = self.obj.get('text')
        sug = ""
        num_mod =len(self.obj.get('modificadores')) if "modificadores" in self.obj else 0
        for i in range(num_mod):
            mod = self.obj['modificadores'][i]
            texto = texto + " " + self._getTextoMod(mod)
        if "sug" in self.obj:
            sug += " "
            for sg in self.obj["sug"]:
                sug += sg
        return '{0: >4} {1}{2}'.format(self.obj['cant'], texto, sug)


    def getDescripcion(self):
        texto = ''
        sug = ""
        num_mod =len(self.obj.get('modificadores')) if "modificadores" in self.obj else 0
        for i in range(num_mod):
            mod = self.obj['modificadores'][i]
            texto = texto + " " + self._getTextoMod(mod)
        if "sug" in self.obj:
            sug = ", ".join(self.obj["sug"])
        return '{0} {1}'.format(texto, sug)



    def _getTextoMod(self, mod):
        texto = mod.get('text')
        num_mod =len(mod.get('modificadores')) if "modificadores" in mod else 0
        for i in range(num_mod):
            aux = mod['modificadores'][i]
            texto = texto + " " + self._getTextoMod(aux)
        return texto

    def getNumMod(self):
        return len(self.obj["modificadores"])


    def getNumArt(self):
        return self.obj['cant']



class Constructor(EventDispatcher):
    producto = ObjectProperty(None, allownone=True)

    def __init__(self, **kargs):
        super(Constructor, self).__init__(**kargs)
        self.pila_modificadores = []

    def add_modificador(self, obj):
        db = None
        num_preg = len(obj.get("preguntas")) if "preguntas" in obj else 0
        if num_preg > 0:
            mod = Linea(obj)
            db = mod.get_pregunta()
            self.pila_modificadores.append(mod)
        else:
            num = len(self.pila_modificadores)
            mod = None if num == 0 else self.pila_modificadores.pop()
            if mod:
                mod.add_modificador(obj)
                if mod.hay_preguntas():
                    self.pila_modificadores.append(mod)
                    db = mod.get_pregunta()
                else:
                    self.producto.add_modificador(mod.obj)
            else:
                self.producto.add_modificador(obj)

        return db
