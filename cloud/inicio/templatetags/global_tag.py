# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   27-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Filename: admin_extras.py
# @Last modified by:   valle
# @Last modified time: 04-Jan-2018
# @License: Apache license vesion 2.0

from django import template
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.conf import settings
import json
import sys
register = template.Library()


@register.filter(name='addattrs')
def addattrs(field, args):
    attr = {}
    try:
        args_parse = args.replace("'", '"')
        attr = json.loads(args_parse)
    except Exception as error:
        print error
    return field.as_widget(attrs=attr)

@register.filter('klass')
def klass(ob):
    return ob.field.widget.__class__.__name__



@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class":css})


@register.simple_tag
def brand(tipo):
    if tipo == "title":
        return settings.BRAND_TITLE
    else:
        return settings.BRAND
