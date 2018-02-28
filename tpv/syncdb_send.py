# @Author: Manuel Rodriguez <valle>
# @Date:   02-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 21-Feb-2018
# @License: Apache license vesion 2.0


import config

from valle_libs.valleorm.qson import *
from models.db import *
from datetime import datetime
from kivy.storage.jsonstore import JsonStore
import time
import json
import os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
url_db = os.path.join(path, "db", "sync.json")
db = JsonStore(url_db)


class SyncVentasSender(QSonSender):
    db_name = "ventas"
    url = config.URL_SERVER+"/simpleapi/"

class SyncClasesSender(QSonSender):
    db_name = "clases"
    url = config.URL_SERVER+"/simpleapi/"

def on_success(obj, result):
    if result["success"] == True:
        text_hora = str(datetime.now())
        db.put("db", date=text_hora)
        if "arqueos" in result["add"]:
            borrar_reg()

def sync_send(text_hora):
    ps = Pedidos.filter(query='modify > "%s" AND estado <> "arqueado"' % text_hora)

    qsons = []
    for p in ps:
        qson = QSon("Pedidos", reg=p.toDICT())
        qsons.append(qson)
        for l in p.lineaspedido_set.get():
            qson_child = QSon("LineasPedido", reg=l.toDICT())
            qson.append_child(qson_child)
        for c in p.clientes_set.get():
            qson_child = QSon("Clientes", reg=c.toDICT())
            qson.append_child(qson_child)
            for d in c.direcciones_set.get():
                qson_dir = QSon("Direcciones", reg=d.toDICT())
                qsons.append(qson_dir)

    if len(qsons) > 0:
        qsonsender = SyncVentasSender()
        qsonsender.save(on_success, qsons)

def borrar_reg():
    ps = Arqueos.filter()
    for p in ps:
        for l in p.conteo.get():
            l.delete()
        for c in p.gastos.get():
            c.delete()
        for d in p.pedidosextra.get():
            d.delete()
        for d in p.pedidos.get():
            d.delete()
        p.delete()

def sync_arqueos_send(text_hora):
    ps = Arqueos.filter(query='modify > "%s"' % text_hora)
    qsons = []
    for p in ps:
        qson = QSon("Arqueos", reg=p.toDICT())
        qsons.append(qson)
        for l in p.conteo.get():
            qson_child = QSon("Conteo", reg=l.toDICT())
            qson.append_child(qson_child)
        for c in p.gastos.get():
            qson_child = QSon("Gastos", reg=c.toDICT())
            qson.append_child(qson_child)
        for d in p.pedidosextra.get():
            qson_dir = QSon("PedidosExtra", reg=d.toDICT())
            qsons.append(qson_dir)
        for d in p.pedidos.get():
            qson_dir = QSon("Pedidos", reg=d.toDICT())
            qsons.append(qson_dir)


    if len(qsons) > 0:
        qsonsender = SyncVentasSender()
        qsonsender.save(on_success, qsons)


if __name__ == '__main__':

    if "db" in db:
        text_hora = db.get("db")["date"]
    else:
        text_hora = str(datetime.now())

    sync_send(text_hora)
    sync_arqueos_send(text_hora)
