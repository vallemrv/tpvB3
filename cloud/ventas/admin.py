# @Author: Manuel Rodriguez <valle>
# @Date:   13-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 30-Sep-2017
# @License: Apache license vesion 2.0


# Register your models here.
from django.contrib import admin
from django.apps import apps
from models import *



@admin.register(Arqueos)
class ArqueosAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'caja_dia', "efectivo", "targeta", "cambio", "descuadre")
    fields = ('caja_dia', "efectivo", "targeta", "cambio", "descuadre", "conteo")


class DireccionInline(admin.TabularInline):
    model = Direcciones

@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ("telefono", 'nombre', "email", "direccion_principal", "pedidos_totales")
    fields = ('nombre', "apellido", "email", "telefono", "nota",)
    inlines = [
        DireccionInline
    ]


@admin.register(Conteo)
class ConteoAdmin(admin.ModelAdmin):
    list_display = ('can', "tipo", "total")

@admin.register(Gastos)
class GastoAdmin(admin.ModelAdmin):
    list_display = ("modify", 'des', "gasto")
    list_filter =  ('modify', "des")
    search_fields = ('modify', "des")

@admin.register(PedidosExtra)
class PedidosExtraAdmin(admin.ModelAdmin):
    list_display = ("importe", 'modo_pago', "numero_pedido")
