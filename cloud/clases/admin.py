# @Author: Manuel Rodriguez <valle>
# @Date:   04-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 10-Mar-2018
# @License: Apache license vesion 2.0

# Register your models here.
from django.contrib import admin
from django.apps import apps
from .models import *

class PreguntasInline(admin.TabularInline):
    model = Preguntas

@admin.register(ClasesPreguntas)
class ClasePreguntasAdmin(admin.ModelAdmin):
    list_display = ('nombre', "preguntas")
    inlines = [
        PreguntasInline,
    ]

class FamiliasInline(admin.TabularInline):
    model = Productos

@admin.register(Familias)
class FamiliasAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    inlines = [
        FamiliasInline,
    ]

class IngredientesInline(admin.TabularInline):
    model = Ingredientes

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'color', 'promocion', "nombre_familia")
    search_fields = ("nombre",)
    list_filter = ("familias",)
    inlines = [
        IngredientesInline
    ]


@admin.register(Clases)
class ClasesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'color', 'promocion', "numero_productos")
    search_fields = ("nombre",)
    #filter_horizontal = ('productos',)
