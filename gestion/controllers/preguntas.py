# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   16-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Filename: productos.py
# @Last modified by:   valle
# @Last modified time: 23-Aug-2017
# @License: Apache license vesion 2.0

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, ListProperty, DictProperty
from service.http import  HttpPreguntas, HttpFamiliaPreguntas



class Preguntas(EventDispatcher):
    editor = ObjectProperty(None)
    grupo = DictProperty({})

    def __init__(self, **kargs):
        super(Preguntas, self).__init__(**kargs)
        self.http = HttpPreguntas()
        self.men = 'No hay preguntas creadas para este grupo para crear una pulse +'


    def on_show(self, **args):
        self.editor.title = "Editar preguntas"
        if "ID" in self.grupo:
            id = self.grupo.get('ID')
            self.http.get_all(on_success=self.on_success_get_all, query={'order':'nombre'}, id=id)
            self.editor.show_spin()


    def on_success_get_all(self, req, res):
        reg = res.get('get')['grupopreguntas']
        if len(reg) > 0:
            nombre = self.grupo.get('nombre')
            reg = reg[0]["preguntas"]
            self.editor.set_botones(self.http.get_datos_button(reg))
            self.editor.title = "Editar "+nombre
        self.editor.show_mensaje(self.men)
        self.editor.hide_spin()


    def add_reg(self):
        nombre = self.grupo.get('nombre')
        model = self.http.get_model('Agregar '+ nombre)
        model.model["color"] = self.grupo.get("color")
        self.editor.show_form(model, self.editar_form)

    def edit_reg(self, sel):
        nombre = self.grupo.get('nombre')
        model = self.http.get_model('Editar '+ nombre)
        model.model.update(sel['reg'])
        self.editor.show_form(model, self.editar_form)


    def editar_form(self, model):
        self.http.mod_reg(query=model, on_success=self.on_success_get_all,
                          query_get={'order':'nombre'}, id=self.grupo.get("ID"))
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

class PregutasFamilias(EventDispatcher):
    asociador = ObjectProperty(None)
    parent = DictProperty({})

    def __init__(self, **kargs):
        super(PregutasFamilias, self).__init__(**kargs)
        self.http = HttpFamiliaPreguntas()


    def on_show(self, **args):
        self.asociador.title = "Elegir preguntas"
        self.http.get_all(on_success=self.on_success_get_all, query={'order':'orden'})
        self.asociador.show_spin()



    def on_success_get_all(self, req, res):
        reg = res.get('get')['grupopreguntas']
        self.asociador.hide_spin()
        self.asociador.set_botones(self.http.get_datos_button(reg))

    def on_press(self, reg):
        print reg
