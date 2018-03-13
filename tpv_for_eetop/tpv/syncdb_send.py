# @Author: Manuel Rodriguez <valle>
# @Date:   02-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 10-Mar-2018
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

def on_success(obj, result):
    print ("[DEBUG  ] %s " % result)
    if result["success"] == True:
        text_hora = str(datetime.now())
        db.put("db", date=text_hora)
        if "arqueos" in result["add"]:
            borrar_reg()

def sync_pedidos_send(**condition):
    ps = Pedidos.filter(**condition)
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



    if len(qsons) > 0:
        qsonsender = SyncVentasSender()
        qsonsender.save(on_success, qsons)

def sync_arqueos_send(**condition):
    ps = Arqueos.filter()
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

def sync_clientes_send(**condition):
    clientes = Clientes.filter(**condition)
    qsons = []
    for c in clientes:
        qson = QSon("Clientes", reg=c.toDICT())
        qsons.append(qson)
        for d in c.direcciones_set.get():
            qson_dir = QSon("Direcciones", reg=d.toDICT())
            qson.append_child(qson_dir)

    if len(qsons) > 0:
        qsonsender = SyncVentasSender()
        qsonsender.save(on_success, qsons)


def get_pedidos(text_hora):
    qsonsender = SyncVentasSender()
    qson = QSon("Pedidos", modify__gte=text_hora)
    qson.add_exclude(estado="arqueado")
    qson.append_child(QSon("LineasPedido"))
    cl = QSon("Clientes")
    cl.append_child(QSon("Direcciones"))
    qson.append_child(cl)
    qsonsender.filter(on_success, qson=(qson,))


def sync_pedidos_send_nc():
    ps = Pedidos.filter(estado="PG_")
    qsons = []
    for p in ps:
        p.estado = "AR_"
        qson = QSon("Pedidos", reg=p.toDICT())
        qsons.append(qson)
        for l in p.lineaspedido_set.get():
            qson_child = QSon("LineasPedido", reg=l.toDICT())
            qson.append_child(qson_child)
        for c in p.clientes_set.get():
            qson_child = QSon("Clientes", reg=c.toDICT())
            qson.append_child(qson_child)



    if len(qsons) > 0:
        qsonsender = SyncVentasSender()
        qsonsender.save(on_success, qsons)

if __name__ == '__main__':
    get_pedidos()
