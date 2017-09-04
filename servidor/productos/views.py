from django.shortcuts import render
from django.http import HttpResponse
from models import Productos


# Create your views here.

def index(request):
    return HttpResponse("Servidor activo. Esperando acciones")

def add_seccion(request):
    if request.method == "POST" and "table_name" in request.POST:
        table_name = request.POST.get("table_name")

        return HttpResponse(dumps(res), content_type="application/json")
    else:
        return index(request)

def list_seccion(request):
    pass
