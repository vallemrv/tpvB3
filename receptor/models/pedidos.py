# coding=utf-8
# @Author: Manuel Rodriguez <valle>
# @Date:   02-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 18-Sep-2017
# @License: Apache license vesion 2.0


from valleorm.models import Model
from valleorm.models import  RelationShip
from valleorm.models import Field

class LineasPedido(Model):
    text = Field(dato="",tipo="TEXT")
    des = Field(dato="",tipo="TEXT")
    cant = Field(dato=1,tipo="INTEGER")
    precio = Field(dato=0.0,tipo="REAL")
    total = Field(dato=0.0,tipo="REAL")
    pedido = RelationShip(name="pedido", tipo="ONE")
    servido = Field(dato="False",tipo="TEXT")
    tipo = Field(dato="",tipo="TEXT")
    imprimible =  Field(dato="True",tipo="TEXT")


class Pedido(Model):
    total = Field(dato=0.0,tipo="REAL")
    modo_pago = Field(dato="",tipo="TEXT")
    fecha = Field(dato="",tipo="TEXT")
    num_avisador = Field(dato="",tipo="TEXT")
    para_llevar = Field(dato="", tipo="TEXT")
    numTicket = Field(dato="", tipo="TEXT")
    num_tlf = Field(dato="",tipo="TEXT")
    lineas = RelationShip(name='lineas', tipo="MANY")
    servido = Field(dato="False",tipo="TEXT")
