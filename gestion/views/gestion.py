# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   15-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Filename: menu.py
# @Last modified by:   valle
# @Last modified time: 16-Aug-2017
# @License: Apache license vesion 2.0


from components.pagenavigations import PageManager
from components.buttons import ButtonIcon
import components.resources as res
from controllers.familias import Familias
from controllers.productos import Productos
from controllers.grupopreguntas import GrupoPreguntas
from kivy.properties import ObjectProperty, ListProperty
from kivy.lang import  Builder

Builder.load_string('''
#:import ValleListView components.listview.ValleListView
#:import Botonera components.botonera.Botonera
#:import Familias views.editor.Editor
#:import Selector views.selector.Selector
#:import AddForm views.add_reg.AddForm
<Gestion>:
    menu: _menu
    editor: _editor
    select: _select
    subeditor: _subeditor
    MainPage:
        title: 'Menu'
        ValleListView:
            bgColor: "#ffffff"
            id: _menu
            spacing: -1


    Page:
        id_page: "selector"
        title: _select.title
        show: _select.on_show
        Selector:
            id: _select
            title: 'Elegir'

    Page:
        id_page: "subeditor"
        title: _subeditor.title
        show: _subeditor.on_show
        id: _page_content_subeditor
        Editor:
            lastlevel: True
            name: 'subeditor'
            title: 'Sub editor'
            id: _subeditor
            add_reg_page: _add_reg
            page_content: _page_content_subeditor

    Page:
        id_page: "editor"
        title: _editor.title
        show: _editor.on_show
        id: _page_content_editor
        Editor:
            name: 'editor'
            title: 'editor'
            id: _editor
            add_reg_page: _add_reg
            page_content: _page_content_editor

    AddForm:
        id_page: 'add_reg'
        id: _add_reg

                    ''')

class Gestion(PageManager):
    menu = ObjectProperty(None)
    items = ListProperty([
        {'icon': res.FA_CUBES,
         'text': "Familias",
         'bgColor': '#FFFFFf',
         'nav': 'familias'},
        {'icon': res.FA_CUTLERY,
         'text': "Productos",
         'bgColor': '#FFFFFf',
         'nav': 'productos'},
        {'icon': res.FA_QUESTION,
         'text': "Preguntas",
         'bgColor': '#FFFFFf',
         'nav': 'preguntas'},
        {'icon': res.FA_HANDSHAK_O,
         'text': "Sugerencias",
         'bgColor': '#FFFFFf',
         'nav': 'sugerencias'},
        ])

    def __init__(self, **kargs):
        super(Gestion, self).__init__(**kargs)
        self.familias = Familias()
        self.productos = Productos()
        self.grupopreguntas = GrupoPreguntas()


    def on_menu(self, w, val):
        for item in self.items:
            btn = ButtonIcon(text=item.get('text'), bgColor=item.get('bgColor'),
                             icon=item.get('icon'), orientation='horizontal',
                             color=(0,0,0,1), icon_font_size='30dp',
                             border_size='1dp', font_size='20dp',
                             tag=item, on_press=self.on_press)

            self.menu.add_linea(btn)

    def on_press(self, btn):
        nav = btn.tag.get('nav')
        if nav == 'familias':
            self.familias.editor = self.editor
            self.editor.controller = self.familias
            self.navigate('editor')
        elif nav == 'productos':
            self.productos.editor = self.editor
            self.editor.controller = self.productos
            self.productos.select = self.select
            self.select.controller = self.productos
            self.navigate('selector')
        elif nav == 'preguntas':
            self.grupopreguntas.editor = self.editor
            self.editor.controller = self.grupopreguntas
            self.navigate('editor')

    def show_subeditor(self, controller):
        controller.editor = self.subeditor
        self.subeditor.controller = controller
        self.navigate('subeditor')
