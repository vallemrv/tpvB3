# @Author: Manuel Rodriguez <valle>
# @Date:   02-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 10-Mar-2018
# @License: Apache license vesion 2.0

import config
import json

from kivy.storage.jsonstore import JsonStore
from models.db import Clases, Productos, Ingredientes, ClasesPreguntas, Preguntas
from valleorm.qson import  QSonSender, QSon



class ClasesSender(QSonSender):
    db_name = "clases"
    url = config.URL_SERVER+"/simpleapi/"
    token = ""


def on_success(obj, result):
    clases =  result.get("get")

    db = JsonStore("../db/clases.json")
    lista = []
    for clase in clases.get("clases"):
        row_clase = {
            'text': clase["nombre"],
            'bgColor': clase["color"],
            'tipo': 'clase',
            "preguntas": []
        }
        if "precio" in clase:
            row_clase["precio"] = clase["precio"]
        if "promocion" in clase:
            row_clase["promocion"] = clase["promocion"]
        lista.append(row_clase)

        row_clase['productos'] = unicode(clase["nombre"])
        db_pro = JsonStore(u"../db/productos/{0}.json".format(unicode(clase["nombre"])))
        lista_productos = []
        for pro in clase["productos"]:
            row = {
                'text': pro["nombre"],
                'bgColor': pro["color"],
                'preguntas': [],
                'modificadores': [],
                'tipo': clase["nombre"].lower()
            }
            if "precio" in pro:
                row["precio"] = pro["precio"]
            if "promocion" in clase:
                row["promocion"] = clase["promocion"]

            if len(pro['ingredientes']) > 0:
                row["ingredientes"] = pro['nombre']
                db_ing = JsonStore(u"../db/ingredientes/{0}.json".format(unicode(pro['nombre'])))
                lista_ing = []
                for ing in pro["ingredientes"]:
                    row_ing = {
                        'text': ing["nombre"],
                        'bgColor': ing["color"],
                        "precio" : ing["precio"] if "precio" in ing else 0
                    }
                    lista_ing.append(row_ing)
                db_ing.put("selectable", estado=True)
                db_ing.put("db", lista=lista_ing)

            lista_productos.append(row)

        db_pro.put("db", lista=lista_productos)

        row_clase["preguntas"] = []
        for clase_preg in clase["clasespreguntas"]:
            nombre = clase_preg["nombre"]
            row_clase["preguntas"].append(nombre)
            db_pre = JsonStore(u"../db/preguntas/{0}.json".format(unicode(nombre)))
            lista_preg = []
            for preg in clase_preg["preguntas"]:
                row_ing= {
                    'text': preg["nombre"],
                    'bgColor': preg["color"],
                }
                if "precio" in preg:
                    row_ing["precio"] = preg["precio"]

                lista_preg.append(row_ing)

            db_pre.put("db", lista=lista_preg)

    db.put('db', lista=lista)


def get_clases():
    sender = ClasesSender()
    qson = QSon("Clases")
    qson_p = QSon("Productos")
    qson_p.append_child(QSon("Ingredientes"))
    qson.append_child(qson_p)
    qson_p = QSon("ClasesPreguntas")
    qson_p.append_child(QSon("Preguntas"))
    qson.append_child(qson_p)
    sender.filter(on_success, qson=(qson,), wait=True)

get_clases()
