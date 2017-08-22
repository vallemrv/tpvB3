# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   16-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Filename: productos.py
# @Last modified by:   valle
# @Last modified time: 16-Aug-2017
# @License: Apache license vesion 2.0

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty
from service.http import HttpFamiliaPreguntas


class GrupoPreguntas(EventDispatcher):
    editor = ObjectProperty(None)

    def __init__(self, **kargs):
        super(GrupoPreguntas, self).__init__(**kargs)
        self.http = HttpFamiliaPreguntas()
        self.men = 'No hay nigun grupo de preguntas creadas para crear uno pulse +'


    def add_reg(self):
        model = self.http.get_model('Agregar Grupo')
        self.editor.show_form(model, self.editar_form)

    def edit_reg(self, sel):
        model = self.http.get_model('Editar Grupo')
        model.model.update(sel['reg'])
        self.editor.show_form(model, self.editar_form)


    def editar_form(self, model):
        self.http.mod_reg(query=model, on_success=self.on_success_get_all,
                          query_get={'order':'orden'})
        self.editor.back_page()
        self.editor.show_spin()


    def on_show(self, **args):
        self.editor.title = "Editar Grupo"
        self.http.get_all(on_success=self.on_success_get_all, query={'order':'orden'})
        self.editor.show_spin()



    def on_success_get_all(self, req, res):
        reg = res.get('get')['grupopreguntas']
        self.editor.hide_spin()
        self.editor.set_botones(self.http.get_datos_button(reg))
        self.editor.show_mensaje(self.men)



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
