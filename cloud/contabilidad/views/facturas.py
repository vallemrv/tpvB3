# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   01-Jan-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 07-Jan-2018
# @License: Apache license vesion 2.0

from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from contabilidad.models import Albaranes, Proveedores
from contabilidad.forms import AlbaranForm
import os

# Create your views here.
@login_required(login_url='login_tk')
def al_elegir_proveedor(request):
    return render(request, "contabilidad/albaranes/find_proveedor.html")

@login_required(login_url='login_tk')
def albaranes(request, id=-1):
    p = get_proveedor_activo(request)
    filter_query = Albaranes.objects.filter(Q(cuenta_id=p.pk))
    if not request.method == "POST" and id == -1:
        f = AlbaranForm()
        return render(request, 'contabilidad/albaranes/listado.html',
                      {"form": f,
                       "p": p,
                       'query': filter_query,
                       "mensaje": "Albaran nuevo" })

    elif not request.method == "POST" and id > 0:
        f = AlbaranForm()
        try:
            obj = Albaranes.objects.get(pk=id)
            f = AlbaranForm(instance=obj)
        except:
            pass
        return render(request, 'contabilidad/albaranes/listado.html',
                      {"form": f,
                       "p": p,
                       'query': filter_query,
                       "mensaje": "Editar albaran" })
    elif id > 0:
        f = AlbaranForm()
        try:
            reg = Albaranes.objects.get(pk=id)
            f = AlbaranForm(request.POST, request.FILES, instance=reg)
        except:
            pass
        if f.is_valid():
            reg = f.save()
            reg.save()
        else:
            print f.errors
        return redirect("Conta:lista_albaranes")
    else:
        f = AlbaranForm(request.POST, request.FILES)
        if f.is_valid():
            obj = f.save(commit=False)
            obj.cuenta_id = p.pk
            obj.save()
        else:
            print f.errors
        return redirect("Conta:lista_albaranes")


@login_required(login_url='login_tk')
def rm_albaran(request, id):
    try:
        obj = Albaranes.objects.get(pk=id)
        if obj.doc.name != "":
            os.remove(os.path.join(settings.MEDIA_ROOT, obj.doc.name))
        obj.delete()
    except Exception as e:
        print e

    return redirect("Conta:lista_albaranes")


@login_required(login_url='login_tk')
def lista_albaranes(request):
    obj = get_proveedor_activo(request)
    f = AlbaranForm()
    if request.method == "POST":
        filter = request.POST["filter"]
        filter_query = Albaranes.objects.filter(Q(cuenta_id=obj.pk) |
                                                Q(fecha__contains=filter) |
                                                Q(numero__contains=filter))
        return render(request, "contabilidad/albaranes/listado.html",
                      {'query': filter_query,
                       "form": f,
                       "p": obj,
                       "mensaje": "Albaran nuevo"})
    else:
        filter_query = Albaranes.objects.filter(Q(cuenta_id=obj.pk))
        return render(request, "contabilidad/albaranes/listado.html",
                      {'query': filter_query,
                       "form": f,
                       'p': obj,
                       "mensaje": "Albaran nuevo" })




@login_required(login_url='login_tk')
def find_albaran(request):
    if request.method == "POST":
        filter = request.POST["filter"]
        filter_query = Albaranes.objects.filter(Q(importe__contains=filter) |
                                                Q(fecha__contains=filter))
        return render(request, "contabilidad/albaranes/lista_ajax.html",
                      {'query': filter_query,
                       "opcion": 'find'})
    else:
        filter_query = Albaranes.objects.all()
        return render(request, "contabilidad/albaranes/lista_ajax.html",
                      {'query': filter_query,
                       "opcion": 'find'})

@login_required(login_url='login_tk')
def view_doc_albaran(request, id):
    print id
    try:
        obj = Albaranes.objects.get(pk=id)
    except Exception as e:
        print e
    file_rml = os.path.join(settings.MEDIA_ROOT, obj.doc.name )
    f = open(file_rml, "rb")
    response = HttpResponse(content_type='image/*')
    response['Content-Disposition'] = 'inline; filename="%s"' % os.path.basename(obj.doc.name)

    response.write(f.read())
    return response

def viewer_img_albaran(request, id):
    try:
        obj = Albaranes.objects.get(pk=id)
    except Exception as e:
        print e
    return render(request, "contabilidad/albaranes/image.html",{
        "obj": obj
    })


def get_proveedor_activo(request):
    pk = request.session["accion_pk_proveedor"] if 'accion_pk_proveedor' in request.session else 0
    obj = Proveedores()
    try:
        obj = Proveedores.objects.get(pk=pk)
    except Exception as e:
        print e

    return obj
