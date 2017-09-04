from __future__ import unicode_literals

from django.db import models

# Create your models here.

class GrupoPregunta(models.Model):
    titulo = models.CharField(max_length=100)
    orden = models.IntegerField()



class Productos(models.Model):
    preguntas = models.ManyToManyField(GrupoPregunta)
    nombre = models.CharField(max_length=200)
    orden = models.IntegerField()
    color = models.CharField(max_length=9)
    precio = models.CharField(max_length=25)
    impresora = models.CharField(max_length=50)


class Secciones(models.Model):
    nombre = models.CharField(max_length=200)
    orden = models.IntegerField()
    color = models.CharField(max_length=9)
    titulo = models.CharField(max_length=100)
    promocion = models.CharField(max_length=10)
    preguntas = models.ManyToManyField(GrupoPregunta)
    productos = models.ManyToManyField(Productos)


class Preguntas(models.Model):
    nombre = models.CharField(max_length=200)
    color = models.CharField(max_length=9)
    incremento = models.CharField(max_length=25)
    grupo = models.ForeignKey(GrupoPregunta, on_delete=models.CASCADE)
    orden = models.IntegerField()


class Ignore(models.Model):
    relProd = models.ForeignKey(Productos, on_delete=models.CASCADE)
    relMod = models.ForeignKey(Preguntas, on_delete=models.CASCADE)
