# @Author: Manuel Rodriguez <valle>
# @Date:   02-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 26-Sep-2017
# @License: Apache license vesion 2.0

import config
import requests
import json

from kivy.storage.jsonstore import JsonStore


data = {
    'token': config.TOKEN_API,
    'user': config.TOKEN_USER,
    'data': ""
    }

def get_clases():
    get_clases={
        "get":{
            'db': "clases",
            "clases":{
                "order": "orden",
                'productos':{"order": "orden, nombre",
                             "ingredientes":{"order": "orden, nombre"}
                             },
                'clasespreguntas':{
                    "preguntas":{"order": "orden, nombre"}
                }
              }
            }
        }
    data['data'] = json.dumps(get_clases)
    r = requests.post(config.URL_SERVER+"/themagicapi/qson_django/", data=data)
    clases = r.json()
    db = JsonStore("../db/clases.json")
    lista = []
    for clase in clases.get('get')["clases"]:

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
                        "precio" : ing["precio"]
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

def get_token(username, password):
    data = {
        "username" : username,
        "password": password
    }

    r = requests.post(config.URL_SERVER+"/token/new.json", data=data)
    print r.json()


get_clases()
#get_token("btres","calamatraca")
