# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   11-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 13-Sep-2017
# @License: Apache license vesion 2.0


from valleorm.django import models

class Pedidos(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    modo_pago = models.CharField(max_length=50)
    para_llevar = models.CharField(max_length=50)
    num_avisador = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    estado = models.CharField(max_length=10, default="PG_NO")
    entrega = models.DecimalField(max_digits=20, decimal_places=2)
    cambio = models.DecimalField(max_digits=20, decimal_places=2)
    modify = models.DateTimeField(auto_now=True)



class Clientes(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20)
    nota = models.TextField(null=True)
    pedidos = models.ManyToManyField(Pedidos)
    fecha_add = models.DateField(auto_now_add=True)
    modify = models.DateTimeField(auto_now=True)
    direccion = models.IntegerField(null=True)


class Direcciones(models.Model):
    direccion = models.CharField(max_length=150)
    localidad = models.CharField(max_length=50, default="Grandada", null=True)
    codigo = models.CharField(max_length=10, null=True)
    clientes = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    modify = models.DateTimeField(auto_now=True)



class LineasPedido(models.Model):
    text = models.CharField(max_length=50)
    des = models.TextField(null=True)
    cant = models.IntegerField()
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    tipo = models.CharField(max_length=50)
    pedidos = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    modify = models.DateTimeField(auto_now=True)
