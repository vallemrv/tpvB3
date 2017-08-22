# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   21-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Filename: model.py
# @Last modified by:   valle
# @Last modified time: 16-Aug-2017
# @License: Apache license vesion 2.0

from kivy.event import EventDispatcher
from kivy.properties import DictProperty, StringProperty, ListProperty


class ContentModel(EventDispatcher):
    model = DictProperty({})
    title = StringProperty("None")
    columns = ListProperty(None)
    tmpl = DictProperty(None)

    @staticmethod
    def normalizar(model):
        return model


class FamiliasModel(ContentModel):
    def __init__(self, **kargs):
        super(FamiliasModel, self).__init__(**kargs)
        self.model = {
            'nombre': '',
            'promocion':'' ,
            'precio':'',
            'color': "#d898e8",
            'orden': ""
        }

        self.columns= ['nombre', 'promocion', 'precio', 'color', 'orden']
        self.tmpl = {
            'color': {
                'type_input':'color',
            }
        }

    @staticmethod
    def normalizar(model):
        model["precio"] = -1.0 if model["precio"] == '' else model["precio"]
        str(model["precio"]).replace(",", ".")
        model["orden"] = 0 if model["orden"] == '' else model["orden"]
        model["promocion"] = -1.0 if model["promocion"] == '' else model["promocion"]
        str(model["promocion"]).replace(",", ".")
        return model

class ProductosModel(ContentModel):
    def __init__(self, **kargs):
        super(ProductosModel, self).__init__(**kargs)
        self.model = {
            'nombre': '',
            'promocion': "",
            'precio': "",
            'color': "#d898e8",
            'orden': "",
            'tieneing': ""
        }

        self.columns= ['nombre', 'promocion', 'precio', 'color', 'orden', 'tieneing']
        self.tmpl = {
            'color': {
                'type_input':'color',
            },
            'tieneing': {
                'label': "Contiene ingredientes",
                'type_control': 'checkbox'
            }
        }

    @staticmethod
    def normalizar(model):
        model["precio"] = 0.0 if model["precio"] == '' else model["precio"]
        str(model["precio"]).replace(",", ".")
        model["orden"] = 0 if model["orden"] == '' else model["orden"]
        model["promocion"] = -1.0 if model["promocion"] == '' else model["promocion"]
        str(model["promocion"]).replace(",", ".")
        return model


class IngredientesModel(ContentModel):
    def __init__(self, **kargs):
        super(IngredientesModel, self).__init__(**kargs)
        self.model = {
            'nombre': '',
            'precio': "",
            'color': "#d898e8",
            'orden': '',
        }

        self.columns= ['nombre',  'precio', 'color', 'orden']
        self.tmpl = {
            'color': {
                'type_input':'color',
            }
    }

    @staticmethod
    def normalizar(model):
        model["precio"] = 0.0 if model["precio"] == '' else model["precio"]
        str(model["precio"]).replace(",", ".")
        model["orden"] = 0 if model["orden"] == '' else model["orden"]
        return model

class FamiliaPreguntasModel(ContentModel):
    def __init__(self, **kargs):
        super(FamiliaPreguntasModel, self).__init__(**kargs)
        self.model = {
            'nombre': '',
            'color': "#d898e8",
            'orden': '',
        }

        self.columns= ['nombre',   'color', 'orden']
        self.tmpl = {
            'color': {
                'type_input':'color',
            }
    }

    @staticmethod
    def normalizar(model):
        model["orden"] = 0 if model["orden"] == '' else model["orden"]
        return model

class PreguntasModel(ContentModel):
    def __init__(self, **kargs):
        super(PreguntasModel, self).__init__(**kargs)
        self.model = {
            'nombre': '',
            'precio': "",
            'color': "#d898e8",
            'orden': '',
        }

        self.columns= ['nombre',  'precio', 'color', 'orden']
        self.tmpl = {
            'color': {
                'type_input':'color',
            }
    }

    @staticmethod
    def normalizar(model):
        model["precio"] = 0.0 if model["precio"] == '' else model["precio"]
        str(model["precio"]).replace(",", ".")
        model["orden"] = 0 if model["orden"] == '' else model["orden"]
        return model
