# -*- coding: utf-8 -*-

"""Programa Gestion para el TPV del Btres

    Autor: Manuel Rodriguez
    Licencia: Apache v2.0

"""
from __future__ import unicode_literals

from valle.models.registro import Registro
from valle.models.campos import Campo
from valle.models.relationship import RelationShip

class Preguntas(Registro):
    nombre = Campo(dato="", tipo="TEXT")
    incremento = Campo(dato=0.0, tipo="REAL")
    color = Campo(dato="", tipo="TEXT")
    grupo = RelationShip(tableName="grupopreguntas", tipo="ONE",
                         relacion="IDGrupo")
    orden = Campo(dato=0, tipo="INTEGER")


class Ignore(Registro):
    grupo = RelationShip(tableName="grupopreguntas", tipo="ONE",
                         relacion="IDGrupo")
    IDPadre = Campo(dato=0, tipo="INTEGER")

class GrupoPreguntas(Registro):
    titulo = Campo(dato="", tipo="TEXT")
    IDPadre = Campo(dato=-1, tipo="INTEGER")
    preguntas = RelationShip(clase=Preguntas, relacion="IDGrupo", tipo="MANY")


class Productos(Registro):
    nombre = Campo(dato="", tipo="TEXT")
    precio = Campo(dato=0.0, tipo="REAL")
    color = Campo(dato="", tipo="TEXT")
    impresora = Campo(dato="", tipo="TEXT")
    orden = Campo(dato=0, tipo="INTEGER")
    seccion = RelationShip(tableName="secciones", tipo="ONE",
                           relacion="IDSeccion")
    ignore = RelationShip(clase=Ignore, relacion="IDPadre", tipo="MANY")
    preguntas = RelationShip(clase=GrupoPreguntas, relacion="IDPadre", tipo="MANY")


class Secciones(Registro):
    nombre = Campo(dato="", tipo="TEXT")
    titulo = Campo(dato="", tipo="TEXT")
    promocion = Campo(dato=1, tipo="INTEGER")
    orden = Campo(dato=0, tipo="INTEGER")
    color = Campo(dato="", tipo="TEXT")
    productos = RelationShip(clase=Productos, relacion="IDSeccion", tipo="MANY")
    preguntas = RelationShip(clase=GrupoPreguntas, relacion="IDPadre", tipo="MANY")
