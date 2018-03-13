# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   01-Mar-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 13-Mar-2018
# @License: Apache license vesion 2.0

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "valle_libs"))
sys.path.insert(0, os.path.join(ROOT_DIR, "tpv"))



from time import sleep
from kivy.lib import osc
from valle_libs.valleorm.qson import *
from models.db import *
from datetime import datetime, timedelta
from kivy.storage.jsonstore import JsonStore
from kivy.core import Logger
from config import config
import websocket
import threading
import time
import json

url_db = os.path.join("../db", "sync.json")
db = JsonStore(url_db)
finalizar = False
stop = threading.Event()

if not os.path.isfile("run.block"):
    f = open("run.block", "w")
    f.close()


class SyncVentasSender(QSonSender):
     db_name = "ventas"
     #url = config.URL_SERVER+"/simpleapi/"
     url = "http://localhost:8000/simpleapi/"


def save_date_db(**args):
    global db
    text_hora_pedidos = args["pedidos"] if "pedidos" in args else db.get("db")["pedidos"]
    text_hora_lineas = args["lineas"] if "lineas" in args else db.get("db")["lineas"]
    text_hora_clientes =args["clientes"] if "clientes" in args else db.get("db")["clientes"]
    text_hora_dir = args["dir"] if "dir" in args elsedb.get("db")["dir"]
    db.put("db", pedidos=text_hora_pedidos, lineas=text_hora_lineas,
                 clientes=text_hora_clientes, dir=text_hora_dir)

def on_success(obj, result):
    if result["success"] == True:
        if "add" in result:
            text_hora_get = db.get("db")["date_get"]
            db.put("db", date=str(datetime.now()), date_get=text_hora_get)
            if "arqueos" in result["add"]:
                borrar_reg()
        if "get" in result:
            text_hora = db.get("db")["date"]
            db.put("db", date_get=str(datetime.now()), date=text_hora)
            for s in  result["get"]["pedidos"]:
                p = Pedidos(**s)
                p.estado = p.estado + "_SN"
                p.save()
                for c in s["clientes"]:
                    cliente = Clientes(**c)
                    cliente.save()
                    for d in c["direcciones"]:
                        direccion = Direcciones(**d)
                        direccion.save()
                for l in s["lineaspedido"]:
                    linea = LineasPedido(**l)
                    linea.save()
                    p.lineaspedido_set.add(linea)


def sync_pedidos_send(**condition):
    ps = Pedidos.filter(**condition)
    qsons = []
    for p in ps:
        p.estado = p.estado + "_SN"
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
                qson_child.append_child(qson_dir)

    qsonsender = SyncVentasSender()
    if len(qsons) > 0:
        qsonsender.save(*qsons)
    return qsonsender

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
            qson.append_child(qson_dir)
        for d in p.pedidos.get():
            qson_dir = QSon("Pedidos", reg=d.toDICT())
            qson.append_child(qson_dir)


    if len(qsons) > 0:
        qsonsender = SyncVentasSender()
        qsonsender.save(*qsons)
        qsonsender.send_data(on_success)


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
        qsonsender.save(*qsons)
        qsonsender.send_data(on_success)

def borrar_reg():
     for p in Arqueos.filter():
         p.delete()
     for d in Pedidos.filter():
         d.delete()
     for p in PedidosExtra.filter():
         p.delete()
     for p in Conteo.filter():
         p.delete()
     for p in Gastos.filter():
         p.delete()



def thread_load():
    global db
    while True:
        try:
            if stop.is_set():
                if os.path.isfile("run.block"):
                    os.unlink("run.block")
                return

            if "db" in db:
                text_hora_pedidos = db.get("db")["pedidos"]
                text_hora_lineas = db.get("db")["lineas"]
                text_hora_clientes = db.get("db")["clientes"]
                text_hora_dir = db.get("db")["dir"]
            else:
                text_hora_pedidos = str(datetime.now()-timedelta(hours=12))
                text_hora_lineas = str(datetime.now()-timedelta(hours=12))
                text_hora_clientes = str(datetime.now()-timedelta(hours=12))
                text_hora_dir = str(datetime.now()-timedelta(hours=12))
                save_date_db(pedidos=text_hora_pedidos,
                             lineas=text_hora_pedidos, clientes=text_hora_pedidos,
                             dir=text_hora_pedidos,)


             '''
            #Envio los pedidos modificados en el tpv
            #query = "modify > '%s'"  % text_hora
            #qsonsender = sync_pedidos_send(query=query + "AND estado NOT LIKE '%_SN%'")

            #Envio la peticion de pedidos modificados fuera del tpv
            qsonsender = QSonSender()
            qsons = []
            qson = QSon("Pedidos", modify__gt=text_hora)
            qson.add_exclude(estado="AR_")
            qsons.append(qson)
            qsons.append(QSon("LineasPedido"))
            qsons.append(QSon("Clientes"))
            qsons.append(QSon("Direcciones"))
            qsonsender.filter(*qsons)
            qsonsender.send_data(on_success)
            '''
            sleep(1)
        except Exception as e:
            Logger.error("[ERROR ] %s" %e)
            sleep(1)

def sync_service(message, *args):
    global finalizar
    if message[2] == "finalizar":
        finalizar = True
    elif message[2] == "sync":
        qsonsender = QSonSender()
        qsonsender.send(on_success, message[3])
    elif message[2] == "sync_arqueo":
        sync_arqueos_send()

    Logger.debug("got a message! %s" % message[2])


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ROOT_DIR = os.path.dirname(BASE_DIR)

    osc.init()
    oscid = osc.listen(ipAddr='127.0.0.1', port=config.PORT_SERVICE)
    osc.bind(oscid, sync_service, '/sync_service')

    thread = threading.Thread(target=thread_load)
    thread.start()

    while not finalizar:
        osc.readQueue(oscid)
        sleep(.1)

    stop.set()
