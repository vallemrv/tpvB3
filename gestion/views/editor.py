# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   25-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Filename: editor.py
# @Last modified by:   valle
# @Last modified time: 16-Aug-2017
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from components.mens import FloatMen
from kivy.animation import Animation
from kivy.lang import Builder

Builder.load_string('''
#:import FloatButton  components.buttons.FloatButton
#:import Botonera components.botonera
#:import Spin components.spin
<Editor>:
    btn_preg: _btn_preg
    btn_ing: _btn_ing
    btn_edit: _btn_edit
    btn_trash: _btn_trash
    spin: _spin
    content: _content_men
    botonera: _botonera
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        Botonera:
            id: _botonera
            scrollable: True
            cols: 2
            font_size: '20dp'
            size_hint: .9, 1
            title: 'None'
            selectable: True
            on_selected: root.on_selected(self, self.selected)


    AnchorLayout:
        anchor_x: 'right'
        anchor_y: 'bottom'
        AnchorLayout:
            anchor_y: 'center'
            anchor_x: 'center'
            size_hint: None, None
            size: dp(70), dp(625)
            GridLayout:
                cols: 1
                size_hint: None, None
                RelativeLayout:
                    size_hint: None, None
                    size: dp(170), dp(70)
                    FloatButton:
                        id: _btn_ing
                        bgColor: '#8ec0fb'
                        icon: res.FA_LEMON
                        size_hint: None, None
                        size: dp(70), dp(70)
                        pos: dp(170), 0
                        on_release: root.edit_ingredientes()
                RelativeLayout:
                    size_hint: None, None
                    size: dp(170), dp(70)
                    FloatButton:
                        id: _btn_preg
                        bgColor: '#8ec0fb'
                        icon: res.FA_QUESTION
                        size_hint: None, None
                        size: dp(70), dp(70)
                        pos: dp(170), 0
                        on_release: root.edit_preguntas()
                RelativeLayout:
                    size_hint: None, None
                    size: dp(170), dp(70)
                    FloatButton:
                        id: _btn_edit
                        bgColor: '#8ec0fb'
                        icon: res.FA_EDIT
                        size_hint: None, None
                        size: dp(70), dp(70)
                        pos: dp(170), 0
                        on_release: root.edit_reg()
                RelativeLayout:
                    size_hint: None, None
                    size: dp(170), dp(70)
                    FloatButton:
                        id: _btn_trash
                        bgColor: '#8ec0fb'
                        icon: res.FA_TRASH
                        size_hint: None, None
                        size: dp(70), dp(70)
                        pos: dp(170), 0
                        on_release: root.rm_reg()
                FloatButton:
                    bgColor: '#8ec0fb'
                    icon: res.FA_PLUS
                    size_hint: None, None
                    size: dp(70), dp(70)
                    on_release: root.add_reg()

    AnchorLayout:
        id: _content_men
    Spin:
        id: _spin

                    ''')

class Editor(AnchorLayout):
    page_manager = ObjectProperty(None)
    add_reg_page = ObjectProperty(None)
    controller = ObjectProperty(None)
    name = StringProperty("editor")
    lastlevel = BooleanProperty(False)

    def __init__(self, **kargs):
        super(Editor, self).__init__(**kargs)
        self.mensaje = FloatMen(men="")

    def rm_reg(self):
        if self.controller:
            self.controller.rm_reg(self.botonera.item_selected)

    def add_reg(self):
        if self.controller:
            self.controller.add_reg()

    def edit_reg(self):
        if self.controller:
            self.controller.edit_reg(self.botonera.item_selected[0].tag)

    def edit_ingredientes(self):
        if self.controller and hasattr(self.controller, 'edit_ingredientes'):
            self.controller.edit_ingredientes(self.botonera.item_selected[0].tag)

    def edit_preguntas(self):
        if self.controller and hasattr(self.controller, 'edit_preguntas'):
            self.controller.edit_preguntas(self.botonera.item_selected[0].tag)


    def show_mensaje(self, men):
        reg = self.botonera.botones
        if len(reg) <= 0 and not self.mensaje in self.content.children:
            self.mensaje.men = men
            self.content.add_widget(self.mensaje)
        elif len(reg) > 0 and self.mensaje in self.content.children:
            self.content.remove_widget(self.mensaje)

    def hide_button(self, *buttons):
        for button in buttons:
            ani = Animation(x=150, duration=.1)
            ani.start(button)

    def show_button(self, *buttons):
        for button in buttons:
            ani = Animation(x=0, duration=.1)
            ani.start(button)

    def show_form(self, model, check_form):
        self.add_reg_page.model = model
        self.add_reg_page.check_form = check_form
        self.page_manager.navigate("add_reg")

    def show_spin(self):
        self.spin.show()

    def hide_spin(self):
        self.spin.hide()

    def remove_button(self, btn):
        self.botonera.botones.remove(btn)

    def append_buttons(self, btns):
        self.botonera.botones.extend(btns)

    def set_botones(self, btns):
        self.botonera.botones = btns

    def on_selected(self, w, l):
        if l == 0:
            self.hide_button(self.btn_edit, self.btn_trash,
                             self.btn_preg, self.btn_ing)
        elif l == 1:
            sel = self.botonera.item_selected[0].tag.get("reg")
            if "tieneing" in sel and sel["tieneing"] == "True" and not self.lastlevel:
                self.show_button(self.btn_ing)
            if not self.lastlevel:
                self.show_button( self.btn_preg)
            self.show_button(self.btn_edit, self.btn_trash)
        elif l > 1:
            self.hide_button(self.btn_edit, self.btn_preg, self.btn_ing)
            self.show_button(self.btn_trash)


    def on_show(self, page_manager):
        self.page_manager = page_manager
        if self.controller:
            self.controller.on_show(name=self.name)


    def back_page(self):
        self.page_manager.back_page()
