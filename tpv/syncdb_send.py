# @Author: Manuel Rodriguez <valle>
# @Date:   02-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 13-Sep-2017
# @License: Apache license vesion 2.0

import config
import requests
import json

from kivy.storage.jsonstore import JsonStore

def get_new_token():
    get_token = {
        'username':'btres',
        'password':'calamatraca'
    }
    return get_token

'''
datos_send = {
    "rm":{
        'db': "clases",
        "clases":{

      }
  }
}
'''

def send_clases():
    db = JsonStore("../db/clases.json")
    datos_send = {
        "add":{
            'db': "clases",
            "clases":[]
        }
    }
    for clase in db.get("db")["lista"]:
        datos_send['add']['clases'].append({
            "nombre": clase["text"],
            "color": clase["color"]
        })
    return datos_send



def send_productos():
    datos_send = {
        "add":{
            'db': "clases",
            "familias":{
                "query": "nombre='Bebidas'",
                "productos":[]
          }
      }
    }
    db = JsonStore("../db/productos/bebidas.json")
    for producto in db.get('db')["lista"]:
        datos_send["add"]['familias']['productos'].append({
            "nombre": producto['text'],
            "color": producto["color"],
            "precio": producto["precio"].replace(",", ".")
        })
    return datos_send

def send_ingredientes():
    datos_send = {
        "add":{
            'db': "clases",
            "productos":{
                "id": "29",
                "ingredientes":[]
          }
      }
    }
    db = JsonStore("../db.back/preguntas/ing_burger.json")
    for producto in db.get('db')["lista"]:
        datos_send["add"]['productos']['ingredientes'].append({
            "nombre": producto['text'],
            "color": producto["color"],
            "precio": producto["precio"].replace(",", ".")
        })
    return datos_send




get_data={
    "get":{
        'db': "clases",
        "familias":{
            "query": "nombre='Bebidas'",
            "productos":{}
      }
  }
}
data = {
    'token': '4p9-d0df1e8d292e6a07262d',
    'user': 1,
    'data': json.dumps(send_ingredientes())
    }

#r = requests.post("http://localhost:8000/themagicapi/qson_django/", data=data)
#print r.json()

from models.db import *

Pedidos()
LineasPedido()
Clientes()
Direcciones()
Arqueos()
Conteo()
Gastos()


#print Pedidos.get_model()
print Arqueos.get_model()
pd = Pedidos()
pd.clientes.get()
