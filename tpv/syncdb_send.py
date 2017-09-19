# @Author: Manuel Rodriguez <valle>
# @Date:   02-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 19-Sep-2017
# @License: Apache license vesion 2.0

import config
import requests
import json
from models.db import *
from datetime import datetime
from kivy.storage.jsonstore import JsonStore
import time



data = {
    'token': config.TOKEN_API,
    'user': 1,
    'data': ''
    }

db = JsonStore("../db/sync.json")
if "db" in db:
    text_hora = db.get("db")["date"]
else:
    text_hora = str(datetime.now())
    db.put("db", date=text_hora)

sync = {
    "add" :{
        "db": "ventas",
        "pedidos":[],
        "arqueos":[]
    }
}

p = Pedidos()
modify = p.getAll(query='modify > "%s" AND estado <> "arqueado"' % text_hora)

for m in modify:
    lineas = m.lineaspedido.get()
    pedido_send = m.toDICT()
    sync["add"]["pedidos"].append(pedido_send)
    if len(lineas) > 0:
        pedido_send["lineaspedido"] = []
        for l in lineas:
            pedido_send["lineaspedido"].append(l.toDICT())
    clientes = m.clientes.get()
    if len(clientes) > 0:
        pedido_send["clientes"] = []
        for c in clientes:
            direcciones = c.direcciones.get()
            clientes_sync = c.toDICT()
            if len(direcciones) > 0:
                clientes_sync["direcciones"] = []
                for d in direcciones:
                    clientes_sync["direcciones"].append(d.toDICT())
            pedido_send["clientes"].append(clientes_sync)

a = Arqueos()
arqueos = a.getAll(query='modify > "%s"' % text_hora)

for arq in arqueos:
    conteo = arq.conteo.get()
    arq_send = arq.toDICT()
    sync["add"]["arqueos"].append(arq_send)
    if len(conteo) > 0:
        arq_send["conteo"] = []
        for c in conteo:
            arq_send["conteo"].append(c.toDICT())
    gastos = arq.gastos.get()
    if len(gastos) > 0:
        arq_send["gastos"] = []
        for g in gastos:
            gastos_sync = g.toDICT()
            arq_send["gastos"].append(gastos_sync)
    pedidos = arq.pedidos.get()
    if len(pedidos) > 0:
        arq_send["pedidos"] = []
        for p in pedidos:
            arq_send["pedidos"].append({"id": p.id, "estado": "arqueado"})



try:
    if len(modify) > 0 or len(arqueos) > 0:
        data["data"] = json.dumps(sync)
        r = requests.post(config.URL_SERVER+"/themagicapi/qson_django/", data=data)
        result = r.json()
        if result["success"] == True:
            print result
            text_hora = str(datetime.now())
            db.put("db", date=text_hora)
except:
    pass
