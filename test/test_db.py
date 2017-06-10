# -*- coding: utf-8 -*-
"""Programa Gestion para el TPV del Btres

    Autor: Manuel Rodriguez
    Licencia: Apache v2.0

"""
from __future__ import unicode_literals
import init
from valle.models.registro import Registro
from models.productos import *


sec = Secciones()
sec.nombre.set("lkdjasldkf")
sec.titulo.set("dlksajlskdf")
sec.color.set("dlkajsdlksaj")
sec.orden.set(0)
sec.save()
for row in sec.getAll():
    print row.toDICT()
