# -*- coding: utf-8 -*-
from kivy.event import EventDispatcher
from kivy.properties import (StringProperty, ObjectProperty,
                             ListProperty, NumericProperty,
                             BooleanProperty)

class LineaPedido(EventDispatcher):
    tipo = StringProperty('pizza')
    producto = ObjectProperty(None, allownone=True)
    ingredientes = ListProperty()
    UID = StringProperty('')
    precio = NumericProperty(0.0)
    finalizada = BooleanProperty(False)
    next = StringProperty('seccion')

    def __init__(self, **kargs):
        super(LineaPedido, self).__init__(**kargs)

    def on_producto(self, key, value):
        self.tipo = self.producto.get('tipo')
        if self.tipo == 'pizza':
            self.next = 'diametro'
            self.producto['texto'] = self.producto.get('text')

    def add_modficador(self, mod):
        tipo_modificador = mod.get('tipo')
        if tipo_modificador == 'menu':
            nombre = mod.get('text').lower()
            if nombre == 'solo':
                self.finalizada = True
                self.next = 'seccion'
            if nombre == 'menu':
                self.finalizada = False
                self.next = 'entrantes_menu'
                self.precio = float(str(mod.get('precio')).replace(",", "."))
                self.producto['texto'] = u"{0}\n{1}".format(
                                                    'Menu:',
                                                    self.producto.get('texto'))
            if nombre == 'infantil':
                self.finalizada = False
                self.next = 'bebida_infantil'
                self.precio = float(str(mod.get('precio')).replace(",", "."))
                self.producto['texto'] = u"{0}\n{1}".format(
                                                    'Menu infantil:',
                                                    self.producto.get('text'))

        if tipo_modificador == 'diametro':
            dim = mod.get('text')
            self.producto['texto'] = u"{0} {1}".format(
                                            self.producto.get('texto'), dim)
            self.producto['dim'] = dim
            self.precio = float(str(self.getPrecioDim(dim)).replace(",", "."))
            self.finalizada = False
            self.next = 'menu'


        if tipo_modificador == 'ingredientes':
            pass


    def getTexto(self):
        return u"{0} Precio: {1:.2f} €".format(
                                       self.producto.get('texto'),
                                       self.precio)

    def getPrecioDim(self, dim):
        if dim == 'Normal':
            return self.producto.get('precio1')
        if dim == 'Familiar':
            return self.producto.get('precio2')
        return self.producto.get('precio1')
