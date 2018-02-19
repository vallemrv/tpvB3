# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   27-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Filename: admin_extras.py
# @Last modified by:   valle
# @Last modified time: 06-Jan-2018
# @License: Apache license vesion 2.0

from django import template
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.conf import settings
import json
import sys
register = template.Library()


@register.filter(name='pagado')
def pagado(gasto):
    if gasto.pagado:
        return 'SI'
    else:
        return 'NO'
