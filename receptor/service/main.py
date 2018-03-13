# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   05-Mar-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 07-Mar-2018
# @License: Apache license vesion 2.0

import sys
import os
reload(sys)
sys.setdefaultencoding('UTF8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
os.chdir(BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "valle_libs"))
sys.path.insert(0, os.path.join(BASE_DIR))

from kivy.core.audio import SoundLoader
from time import sleep
from kivy.lib import osc
from kivy.logger import Logger
from valleorm.qson import QSonSender, QSon
from models.pedidos import *

serviceport = 3010
activityport = 3011
finalizar = False

serviceport = 3010
activityport = 3011
finalizar = False

class PedidosSenderQSon(QSonSender):
    db_name = "ventas"
    url = "http://btres.elbrasilia.com/simpleapi/"
    #url = "http://localhost:8000/simpleapi/"
    Pedidos()
    LineasPedido()

def sync_pedidos():
    sound = SoundLoader.load('a1.wav')
    if sound:
        print("Sound found at %s" % sound.source)
        print("Sound is %.3f seconds" % sound.length)
        sound.play()
    osc.sendMsg('/sync_pedidos', ['sync', ], port=activityport)

def close_pedidos(lista_pedidos):
    qsonsender = PedidosSenderQSon()
    qsons = []
    for s in lista_pedidos:
        s["estado"] = s["estado"].replace("NO", "SI")
        qson = QSon("Pedidos", reg=s)
        qsons.append(qson)

    qsonsender.save(*qsons)
    qsonsender.send_data(echo)

def echo(request, val):
    pass

def echo_servido(request, val):
    pass

def esImprimible(val):
    if val.get("tipo") == "bebidas" or val.get("tipo") == "postres":
        return False
    else:
        return True

def got_json(result, val):
    Logger.info('BTRES: '+ str(val))
    if val["success"] == True:
        lista_pedidos = []
        for s in  val["get"]["pedidos"]:
            p = Pedidos(**s)
            p.estado = p.estado.replace("NO", "SI")
            lista_pedidos.append(s)

            for c in s["clientes"]:
                if len(c["direcciones"]) > 0:
                    p.direccion = unicode(c["direcciones"][0]["direccion"]) + '  Tlf:' + c["telefono"]

            p.save()
            for l in s["lineaspedido"]:
                linea = LineasPedido(**l)
                linea.imprimible = esImprimible(l)
                linea.save()
                p.lineaspedido_set.add(linea)

        if len(lista_pedidos) > 0:
            close_pedidos(lista_pedidos)
            sleep(3)
            sync_pedidos()

def servir_linea(id, servido):
    qsonsender = PedidosSenderQSon()
    qson = QSon("LineasPedido", reg={"id":id, "servido":servido})

    qsonsender.save(qson)
    qsonsender.send_data(echo_servido)

def servir_pedido(id):
    qsonsender = PedidosSenderQSon()
    qson = QSon("Pedidos", reg={"id":id, "servido":True})
    qsonsender.save(qson)
    qsonsender.send_data(echo_servido)


def get_pedidos():
    qsonsender = PedidosSenderQSon()
    qson = QSon("Pedidos", estado__icontains="_NO")
    qson.append_child(QSon("LineasPedido"))
    cl = QSon("Clientes")
    cl.append_child(QSon("Direcciones"))
    qson.append_child(cl)
    qsonsender.filter(qson)
    qsonsender.send_data(got_json)

def servidor_men(message, *args):
    global finalizar
    if message[2] == "linea_servida":
        id = message[3]
        servido = message[4]
        servir_linea(id, servido)
    elif message[2] == "pedido_servido":
        id = message[3]
        servir_pedido(id)
    elif message[2] == "finalizar":
        finalizar = True

    print("got a message! %s" % message[2])


if __name__ == '__main__':
    osc.init()
    oscid = osc.listen(ipAddr='127.0.0.1', port=serviceport)
    osc.bind(oscid, servidor_men, '/servidor_men')

    while not finalizar:
        osc.readQueue(oscid)
        try:
            get_pedidos()
        except Exception as e:
            Logger.info('BTRES: '+ str(e))
        sleep(.1)
