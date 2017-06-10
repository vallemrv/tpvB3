from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from kivy.storage.jsonstore import JsonStore
from django.http import HttpResponse
from django.template import loader
import json
import os

# Create your views here.

def index(request):
    from glob import glob
    files = sorted(glob("/home/brasilia/tpvB3/db/pd/*[0,1].11.json"), reverse=True)
    dbs = []
    for f in files:
        dbs.append({"fl":f, 'db':JsonStore(f).get('reg')})
    return HttpResponse(json.dumps(dbs))

@csrf_exempt
def servido(request):
    if request.method == "POST" and "fl" in request.POST:
        aux = request.POST.get("fl")
        nombre = request.POST.get("fl")

        if "0.11." in nombre:
            nombre = nombre.replace("0.11.", "4.11.")
        elif "1.11." in nombre:
            nombre = nombre.replace("1.11.", "3.11.")
        from os import rename
        rename(aux, nombre)

    #index(request)
    return HttpResponse("Hola que pasa")
