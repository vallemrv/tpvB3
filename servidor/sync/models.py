# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone



# Create your models here.

class Sync(models.Model):
    table_name = models.CharField(max_length=200)
    fecha_modificado = models.DateTimeField("Fecha Modificado")

    def toJSON(self):
        res = {"id":self.id, "table_name": self.table_name,
               "fecha_modificado": self.fecha_modificado.strftime("%Y/%m/%d_%H:%M:%S")}
        return res
