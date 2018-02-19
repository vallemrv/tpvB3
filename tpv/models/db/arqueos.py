# @Author: Manuel Rodriguez <valle>
# @Date:   13-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 18-Feb-2018
# @License: Apache license vesion 2.0


from valleorm import models


class Gastos(models.Model):
    des = models.CharField(max_length=100)
    gasto = models.DecimalField(max_digits=20, decimal_places=2)
    modify = models.DateTimeField(auto_now=True)

class Conteo(models.Model):
    can = models.IntegerField()
    tipo =  models.DecimalField(max_digits=20, decimal_places=2)
    total =  models.DecimalField(max_digits=20, decimal_places=2)
    texto_tipo = models.CharField(max_length=100, null=True, blank=True)
    modify = models.DateTimeField(auto_now=True)

class PedidosExtra(models.Model):
    importe = models.DecimalField(max_digits=20, decimal_places=2)
    numero_pedido =  models.IntegerField()
    modo_pago =  models.CharField(max_length=50, null=True, blank=True, default="Efectivo")
    modify = models.DateTimeField(auto_now=True)
    estado =  models.CharField(max_length=50, null=True, blank=True, default="no_arqueado")

class Arqueos(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    caja_dia = models.DecimalField(max_digits=20, decimal_places=2)
    efectivo = models.DecimalField(max_digits=20, decimal_places=2)
    cambio = models.DecimalField(max_digits=20, decimal_places=2)
    total_gastos = models.DecimalField(max_digits=20, decimal_places=2)
    targeta = models.DecimalField(max_digits=20, decimal_places=2)
    descuadre = models.DecimalField(max_digits=20, decimal_places=2)
    pedidos = models.ManyToManyField("Pedidos")
    pedidosextra = models.ManyToManyField(PedidosExtra)
    gastos = models.ManyToManyField(Gastos)
    conteo = models.ManyToManyField(Conteo)
    modify = models.DateTimeField(auto_now=True)
