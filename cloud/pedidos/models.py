# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   08-Mar-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 13-Apr-2018
# @License: Apache license vesion 2.0

from django.db import models

class EstadoOnline(models.Model):
    abierto = models.BooleanField(default=True)
