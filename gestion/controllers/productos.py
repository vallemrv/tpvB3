# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   16-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Filename: productos.py
# @Last modified by:   valle
# @Last modified time: 13-Aug-2017
# @License: Apache license vesion 2.0

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, ListProperty
from service.http import HttpProductos, HttpFamilias
from controllers.ingredientes import Ingredientes
from controllers.preguntas import Preguntas


class Productos(EventDispatcher):
    editor = ObjectProperty(None)
    select = ObjectProperty(None)

    def __init__(self, **kargs):
        super(Productos, self).__init__(**kargs)
        self.http = HttpProductos()
        self.httpFm = HttpFamilias()
        self.men = 'No hay productos creados para esta familia para crear uno pulse +'


    def on_show(self, **args):
        if 'selector' in args and args.get('selector') == True:
            self.httpFm.get_all(on_success=self.on_success_familias_get_all, query={'order':'orden'})
            self.select.title = "Elegir familia"
            self.select.show_spin()

    def on_success_familias_get_all(self, req, res):
        reg = res.get('get')['familias']
        self.select.hide_spin()
        self.select.set_botones(self.httpFm.get_datos_button(reg))
        self.select.show_mensaje("No hay familias creadas. Primero tienes que crear una familia")

    def on_press(self, familia):
        self.familia = familia["reg"]
        id = familia['reg'].get('ID')
        self.http.get_all(on_success=self.on_success_get_all, query={'order':'nombre'}, id=id)
        self.select.page_manager.navigate('editor')
        self.editor.show_spin()


    def on_success_get_all(self, req, res):
        reg = res.get('get')['familias']
        if len(reg) > 0:
            nombre = self.familia.get('nombre')
            reg = reg[0]["lstproductos"]
            self.editor.set_botones(self.http.get_datos_button(reg))
            self.editor.title = "Editar "+nombre
        self.editor.show_mensaje(self.men)
        self.editor.hide_spin()


    def add_reg(self):
        nombre = self.familia.get('nombre')
        model = self.http.get_model('Agregar '+ nombre)
        model.model["color"] = self.familia.get("color")
        self.editor.show_form(model, self.editar_form)

    def edit_reg(self, sel):
        nombre = self.familia.get('nombre')
        model = self.http.get_model('Editar '+ nombre)
        model.model.update(sel['reg'])
        self.editor.show_form(model, self.editar_form)

    def edit_ingredientes(self, sel):
        self.select.page_manager.show_subeditor(Ingredientes(producto=sel.get("reg")))

    def edit_preguntas(self, sel):
        self.select.page_manager.show_subeditor(Pregutas(parent=sel.get("reg")))


    def editar_form(self, model):
        self.http.mod_reg(query=model, on_success=self.on_success_get_all,
                          query_get={'order':'nombre'}, id=self.familia.get("ID"))
        self.editor.back_page()
        self.editor.show_spin()

    def rm_reg(self, regs):
        datos = []
        for reg in regs:
            datos.append(reg.tag['reg'])
            self.editor.remove_button(reg.tag)
        self.http.rm_reg(query=datos, on_success=self.on_success_rm)
        self.editor.show_spin()

    def on_success_rm(self, req, res):
        self.editor.show_mensaje(self.men)
        self.editor.hide_spin()
