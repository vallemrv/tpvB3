# coding=utf-8
# @Author: Manuel Rodriguez <valle>
# @Date:   02-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 26-Feb-2018
# @License: Apache license vesion 2.0


from valleorm import models

class Pedidos(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    modo_pago = models.CharField(max_length=50)
    para_llevar = models.CharField(max_length=50)
    num_avisador = models.CharField(max_length=50)
    direccion = models.CharField(max_length=150,  default="No hay direccion", null=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, null=True, default=0.0)
    estado = models.CharField(max_length=10, default="PG_NO")
    entrega = models.DecimalField(max_digits=20, decimal_places=2, null=True, default=0.0)
    cambio = models.DecimalField(max_digits=20, decimal_places=2, null=True, default=0.0)
    modify = models.DateTimeField(auto_now=True)
    servido = models.BooleanField(default=False)
    def __unicode__(self):
        return u"{0} - {1} - {2}".format(self.id, self.estado, self.total)

    class Meta:
        verbose_name = "Pedido"


class LineasPedido(models.Model):
    text = models.CharField(max_length=50)
    des = models.TextField(null=True)
    cant = models.IntegerField()
    precio = models.DecimalField(max_digits=20, decimal_places=2, null=True, default=0.0)
    total = models.DecimalField(max_digits=20, decimal_places=2, null=True, default=0.0)
    tipo = models.CharField(max_length=50)
    pedidos = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    modify = models.DateTimeField(auto_now=True)
    servido = models.BooleanField(default=False)
    imprimible = models.BooleanField(default=False)
    def __unicode__(self):
        return u"{0} - {1} - {2} - {3}".format(self.cant, self.text, self.precio, self.total)
