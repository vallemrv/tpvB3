# coding=utf-8
from valle.models.registro import Registro
from valle.models.relationship import  RelationShip
from valle.models.campos import Campo

class LineasPedido(Registro):
    text = Campo(dato="",tipo="TEXT")
    des = Campo(dato="",tipo="TEXT")
    cant = Campo(dato=1,tipo="INTEGER")
    precio = Campo(dato=0.0,tipo="REAL")
    total = Campo(dato=0.0,tipo="REAL")
    pedido = RelationShip(tableName="pedido", tipo="ONE",
                         relacion="IDPedido")
    servido = Campo(dato="False",tipo="TEXT")
    tipo = Campo(dato="",tipo="TEXT")
    imprimible =  Campo(dato="True",tipo="TEXT")


class Pedido(Registro):
    total = Campo(dato=0.0,tipo="REAL")
    modo_pago = Campo(dato="",tipo="TEXT")
    fecha = Campo(dato="",tipo="TEXT")
    num_avisador = Campo(dato="",tipo="TEXT")
    para_llevar = Campo(dato="", tipo="TEXT")
    numTicket = Campo(dato="",tipo="TEXT")
    num_tlf = Campo(dato="",tipo="TEXT")
    lineas = RelationShip(clase=LineasPedido, relacion="IDPedido", tipo="MANY")
    servido = Campo(dato="False",tipo="TEXT")
