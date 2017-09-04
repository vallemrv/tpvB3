# @Author: Manuel Rodriguez <valle>
# @Date:   02-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 04-Sep-2017
# @License: Apache license vesion 2.0


from valleorm.django import models

class Clases(models.Model):
    nombre = models.CharField(max_length=50)
    promocion = models.DecimalField(decimal_places=2, default=None, null=True)
    precio = models.DecimalField(decimal_places=2, default=None, null=True)
    color = models.CharField(default="#d898e8")
    orden = models.IntegerField(default=0)
    productos = models.ManyToMany(otherclass='Productos')
    preguntas = models.ManyToMany(otherclass='ClasesPreguntas')
    modify = models.DateTime(auto_now=True)

class Productos(models.Model):
    nombre = models.CharField(max_length=50)
    promocion = models.DecimalField(decimal_places=2, default=None, null=True)
    precio = models.DecimalField(decimal_places=2, default=None, null=True)
    color = models.CharField(default="#d898e8")
    orden = models.IntegerField(default=0)
    preguntas = models.ManyToMany(otherclass='ClasesPreguntas')
    ignore = models.ManyToMany(otherclass='ClasesPreguntas')
    modify = models.DateTime(auto_now=True)


class Ingredientes(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(decimal_places=2, default=None, null=True)
    color = models.CharField(default="#d898e8")
    orden = models.IntegerField(default=0)
    productos = models.ForeingKey(otherclass='Productos', cascade=models.CASCADE)
    modify = models.DateTime(auto_now=True)



class ClasesPreguntas(models.Model):
    nombre = models.CharField(max_length=50)
    modify = models.DateTime(auto_now=True)


class Preguntas(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(decimal_places=2, default=None, null=True)
    color = models.CharField(default="#d898e8")
    orden = models.IntegerField(default=0)
    grupo = models.ForeingKey(otherclass='Preguntas')
    modify = models.DateTime(auto_now=True)
