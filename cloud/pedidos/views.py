# @Author: Manuel Rodriguez <valle>
# @Date:   08-Mar-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 08-Mar-2018
# @License: Apache license vesion 2.0


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(unicode):
    return HttpResponse("Holaaaaaaa cara cola")
