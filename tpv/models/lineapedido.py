# -*- coding: utf-8 -*-
from kivy.event import EventDispatcher
from kivy.properties import (StringProperty, ObjectProperty,
                             ListProperty, NumericProperty,
                             BooleanProperty)
from shared.utils import parse_float

class Linea():
    def __init__(self, obj):
        self.puntero = 0
        self.obj = obj

    def get_pregunta(self):
        db = None
        num = len(self.obj.get("preguntas"))
        if self.puntero < num:
            db = self.obj.get('preguntas')[self.puntero]
            self.puntero = self.puntero + 1
        return db

    def hay_preguntas(self):
        num = len(self.obj.get("preguntas"))
        return self.puntero < num

    def add_modificador(self, obj):
        self.obj['modificadores'].append(obj)

    def getTotal(self):
        total = parse_float(self.obj.get('precio'))
        for i in range(len(self.obj.get('modificadores'))):
            mod = self.obj['modificadores'][i]
            total = total + self._getPrecioMod(mod)
        return total

    def _getPrecioMod(self, mod):
        total = parse_float(mod.get('precio'))
        for i in range(len(mod.get('modificadores'))):
            aux = mod['modificadores'][i]
            total = total + self._getPrecioMod(aux)
        return total

    def getTexto(self):
        texto = self.obj.get('text')
        for i in range(len(self.obj.get('modificadores'))):
            mod = self.obj['modificadores'][i]
            texto = texto + " " + self._getTextoMod(mod)
        return texto

    def _getTextoMod(self, mod):
        texto = mod.get('text')
        for i in range(len(mod.get('modificadores'))):
            aux = mod['modificadores'][i]
            texto = texto + " " + self._getTextoMod(aux)
        return texto



class Constructor(EventDispatcher):
    producto = ObjectProperty(None, allownone=True)

    def __init__(self, **kargs):
        super(Constructor, self).__init__(**kargs)
        self.pila_modificadores = []

    def add_modificador(self, obj):
        db = None
        num = len(obj.get("preguntas"))
        if num > 0:
            mod = Linea(obj)
            db = mod.get_pregunta()
            self.pila_modificadores.append(mod)
        else:
            mod = self.pila_modificadores.pop()
            if mod:
                mod.add_modificador(obj)
                if mod.hay_preguntas():
                    self.pila_modificadores.append(mod)
                    db = mod.get_pregunta()
                else:
                    self.producto.add_modificador(mod.obj)
            else:
                self.producto.add_modificador(mod.obj)

        return db
