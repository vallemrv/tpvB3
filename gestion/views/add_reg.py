# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   20-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Filename: add_reg.py
# @Last modified by:   valle
# @Last modified time: 31-Jul-2017
# @License: Apache license vesion 2.0


from components.pagenavigations import Page
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_string('''
#:import InputForm components.inputform
<AddForm>:
    form: _form
    InputForm:
        id: _form

                    ''')

class AddForm(Page):
    model = ObjectProperty(None)
    check_form = ObjectProperty(None)

    def __init__(self, **kargs):
        super(AddForm, self).__init__(**kargs)

    def on_model(self, w, l):
        self.title = self.model.title
        self.form.add_model(self.model.model, self.model.columns, self.model.tmpl)

    def on_check_form(self, w, val):
        if self.form:
            self.form.on_press = self.check_form
