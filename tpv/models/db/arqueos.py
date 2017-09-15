# @Author: Manuel Rodriguez <valle>
# @Date:   13-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 13-Sep-2017
# @License: Apache license vesion 2.0


from valleorm.django import models


class Gastos(models.Model):
    des = models.CharField(max_length=100)
    gasto = models.DecimalField(max_digits=20, decimal_places=2)
    modify = models.DateTimeField(auto_now=True)

class Conteo(models.Model):
    can = models.IntegerField()
    tipo =  models.DecimalField(max_digits=20, decimal_places=2)
    total =  models.DecimalField(max_digits=20, decimal_places=2)
    texto_tipo = models.EmailField(max_length=100, null=True, blank=True)
    modify = models.DateTimeField(auto_now=True)

class Arqueos(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    caja_dia = models.DecimalField(max_digits=20, decimal_places=2)
    efectivo = models.DecimalField(max_digits=20, decimal_places=2)
    cambio = models.DecimalField(max_digits=20, decimal_places=2)
    total_gastos = models.DecimalField(max_digits=20, decimal_places=2)
    targeta = models.DecimalField(max_digits=20, decimal_places=2)
    descuadre = models.DecimalField(max_digits=20, decimal_places=2)
    pedidos = models.ManyToManyField("Pedidos", main_module="models.db.pedidos")
    gastos = models.ManyToManyField(Gastos)
    conteo = models.ManyToManyField(Conteo)
    modify = models.DateTimeField(auto_now=True)
