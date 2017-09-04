from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Sync
from json import dumps

# Create your views here.

def index(request):
    return HttpResponse("Servidor activo. Esperando acciones")

def list(request):
    res = []
    for obj in Sync.objects.all():
        res.append(obj.toJSON())
    return HttpResponse(dumps(res), content_type="application/json")

@csrf_exempt
def getTime(request):
    if request.method == "POST" and "table_name" in request.POST:
        table_name = request.POST.get("table_name")
        modificado =  request.POST.get("modificado")
        q = Sync.objects.filter(table_name=table_name)
        res = {"modificado": "none"}
        if q.count() > 0:
            f = q[0].fecha_modificado.strftime("%Y/%m/%d_%H:%M:%S")
            if f < modificado:
                res["modificado"] = "okey"
        return HttpResponse(dumps(res), content_type="application/json")
    else:
        return index(request)
