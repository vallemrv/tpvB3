# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   01-Jan-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 09-Jan-2018
# @License: Apache license vesion 2.0

from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Proveedores(models.Model):
    nombre = models.CharField(max_length=100)
    razon_social = models.CharField("Razón social", max_length=100,  blank=True, null=True)
    CIF = models.CharField(max_length=10,  blank=True, null=True)
    direccion = models.CharField("Dirección", max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=12, blank=True, null=True)
    notas = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ["-id"]


class CuentasGastos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField("Descripción", null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ["-id"]

class SubCuentaGastos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField("Descripción", null=True, blank=True)
    gastos = models.ManyToManyField("Gastos")
    cuenta = models.ForeignKey("CuentasGastos", on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre


    class Meta:
        ordering = ["-id"]


class Gastos(models.Model):
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField("Descripción", max_length=150, null=True, blank=True)
    cuenta = models.ForeignKey("CuentasGastos", on_delete=models.CASCADE)
    fecha_apunte = models.DateTimeField(auto_now_add=True)
    fecha_modificado = models.DateField(auto_now=True)
    fecha = models.DateField()
    pagado = models.BooleanField(default=True)

    def __unicode__(self):
        return self.descripcion

    class Meta:
        ordering = ["-fecha"]


class Albaranes(models.Model):
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField("Descripción", max_length=150, null=True, blank=True)
    fecha_apunte = models.DateTimeField(auto_now_add=True)
    fecha = models.DateField()
    fecha_modificado = models.DateField(auto_now=True)
    doc = models.FileField(upload_to='albaranes', null=True, blank=True)
    cuenta = models.ForeignKey("Proveedores", on_delete=models.CASCADE)
    aviso = models.CharField("Aviso", max_length=150, null=True, blank=True)
    pagado = models.BooleanField(default=False)

    def __unicode__(self):
        return self.descripcion

    class Meta:
        ordering = ["-fecha"]

class Facturas(models.Model):
    albaranes = models.ManyToManyField("Albaranes")
    fecha_apunte = models.DateTimeField(auto_now_add=True)
    fecha = models.DateField()
    fecha_modificado = models.DateField(auto_now=True)
    doc = models.FileField(upload_to='facturas', null=True, blank=True)

    class Meta:
        ordering = ["-fecha"]

class SaldoRegulador(models.Model):
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=150)
    fecha_apunte = models.DateTimeField(auto_now_add=True)
    fecha_modificado = models.DateField(auto_now=True)
    cuenta = models.ForeignKey("Proveedores", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-fecha_apunte"]



class Ingresos(models.Model):
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField("Descripción", max_length=50, default="Caja del dia")
    fecha = models.DateField()
    fecha_apunte = models.DateTimeField(auto_now_add=True)
    fecha_modificado = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-fecha_apunte"]
