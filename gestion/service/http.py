# @Author: Manuel Rodriguez <valle>
# @Date:   16-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Filename: http.py
# @Last modified by:   valle
# @Last modified time: 16-Aug-2017
# @License: Apache license vesion 2.0

from utils.models import (FamiliasModel, ProductosModel, PreguntasModel,
                          IngredientesModel, FamiliaPreguntasModel)
from config import config
from kivy.network.urlrequest import UrlRequest
from kivy.event import EventDispatcher
from kivy.properties import DictProperty, StringProperty, ObjectProperty
import json
import urllib

class Http(EventDispatcher):
    headers = DictProperty()
    tbName = StringProperty('')
    data_send = DictProperty()

    def __init__(self, **kargs):
        super(Http, self).__init__(**kargs)
        self.headers = {'Content-type': 'application/x-www-form-urlencoded',
                        'Accept': 'text/json'}

        self.data_send = { 'token': config.token, 'user': config.user}

    def __httprequest__(self, data, on_success):
        data = urllib.urlencode(data)
        r = UrlRequest(url=config.servidor, on_success=on_success, verify=False,
                       req_body=data, req_headers=self.headers, method="POST",
                       on_error=self.on_error)

    def __modify__(self, on_success, query={}, type_query='get', query_get={}, id=None):
        send = {
            type_query:{
                'db': config.db,
                self.tbName: query
                }
        }

        if type_query == 'add':
            send["get"] = {
                'db': config.db,
                self.tbName: query_get
            }
        self.data_send['data'] = json.dumps(send)
        self.__httprequest__(self.data_send, on_success)

    def get_all(self, on_success, query={}, id=None):
        self.__modify__(on_success=on_success,
                        query=query, type_query='get', id=id)

    def add_reg(self, on_success, query, query_get={}, id=None):
        self.__modify__(on_success=on_success, query=query,
                        type_query='add', query_get=query_get, id=id)


    def rm_reg(self, on_success, query, id=None):
        self.__modify__(on_success=on_success, query=query,
                        type_query='rm', id=id)

    def mod_reg(self, on_success, query, query_get={},  id=None):
        self.__modify__(on_success=on_success, query=query,
                        type_query='add', query_get=query_get, id=id)

    def on_error(self, req,  error):
        print 'error', error

    def get_model(self, title):
        pass

class HttpFamilias(Http):
    def __init__(self, **kargs):
        super(HttpFamilias, self).__init__(**kargs)
        self.tbName = 'familias'

    def __modify__(self, on_success, query={}, type_query='get', query_get={}, id=None):
        if type_query == "add":
            query = FamiliasModel().normalizar(query)
        super(HttpFamilias, self).__modify__(on_success, query,
                                             type_query, query_get, id)

    def get_model(self, title):
        model = FamiliasModel()
        model.title = title
        return model

    def get_datos_button(self, regs):
        datos = []
        for reg in regs:
            dato = {
                'bgColor': reg['color'],
                'text': reg['nombre'],
                'reg': reg
            }
            datos.append(dato)
        return datos

class HttpProductos(Http):
    def __init__(self, **kargs):
        super(HttpProductos, self).__init__(**kargs)
        self.tbName = 'productos'

    def __modify__(self,  on_success, query={}, type_query='get', query_get={}, id=None):
        send = {
            type_query:{
                'db': config.db,
                'familias':{
                     'ID': id,
                     'lstproductos':[]
                     }
                }
            }
        if type_query == "get":
            send['get']["familias"]['lstproductos']= {self.tbName: query}

        if type_query == 'add':
            query = ProductosModel.normalizar(query)
            send['add']["familias"]['lstproductos'].append({self.tbName: query})
            send["get"] = {
                'db': config.db,
                'familias':{
                     'ID': id,
                     'lstproductos':
                        {self.tbName: query_get}
                        }
                }
        if type_query == 'rm':
            send['rm'] = {'db': config.db, self.tbName: query}

        self.data_send['data'] = json.dumps(send)
        self.__httprequest__(self.data_send, on_success)

    def get_model(self, title):
        model = ProductosModel()
        model.title = title
        return model

    def get_datos_button(self, regs):
        datos = []
        for reg in regs:
            dato = {
                'bgColor': reg['color'],
                'text': reg['nombre'],
                'reg': reg
            }
            datos.append(dato)
        return datos

class HttpIngredientes(Http):
    def __init__(self, **kargs):
        super(HttpIngredientes, self).__init__(**kargs)
        self.tbName = 'ingredientes'

    def __modify__(self,  on_success, query={}, type_query='get',
                   query_get={}, id=None):
        send = {
            type_query:{
                'db': config.db,
                'productos':{
                     'ID': id,
                     'ingredientes': query
                     }
                }
            }
        if type_query == 'add':
            query = IngredientesModel.normalizar(query)
            send['add']["productos"]['ingredientes'] = query
            send["get"] = {
                'db': config.db,
                'productos':{
                     'ID': id,
                     'ingredientes': query_get
                  }
                }
        if type_query == 'rm':
            send['rm'] = {'db': config.db, self.tbName: query}

        self.data_send['data'] = json.dumps(send)
        self.__httprequest__(self.data_send, on_success)

    def get_model(self, title):
        model = IngredientesModel()
        model.title = title
        return model

    def get_datos_button(self, regs):
        datos = []
        for reg in regs:
            dato = {
                'bgColor': reg['color'],
                'text': reg['nombre'],
                'reg': reg
            }
            datos.append(dato)
        return datos

class HttpFamiliaPreguntas(Http):
    def __init__(self, **kargs):
        super(HttpFamiliaPreguntas, self).__init__(**kargs)
        self.tbName = 'grupopreguntas'

    def __modify__(self,  on_success, query={}, type_query='get',
                   query_get={}, id=None):
        if type_query == "add":
            query = FamiliaPreguntasModel().normalizar(query)

        super(HttpFamiliaPreguntas, self).__modify__(on_success, query,
                                             type_query, query_get, id)


    def get_model(self, title):
        model = FamiliaPreguntasModel()
        model.title = title
        return model

    def get_datos_button(self, regs):
        datos = []
        for reg in regs:
            dato = {
                'bgColor': reg['color'],
                'text': reg['nombre'],
                'reg': reg
            }
            datos.append(dato)
        return datos

class HttpPreguntas(Http):
    def __init__(self, **kargs):
        super(HttpPreguntas, self).__init__(**kargs)
        self.tbName = 'preguntas'

    def __modify__(self,  on_success, query={}, type_query='get',
                   query_get={}, id=None):
        send = {
            type_query:{
                'db': config.db,
                'grupopreguntas':{
                     'ID': id,
                     'preguntas': query
                     }
                }
            }
        if type_query == 'add':
            query = IngredientesModel.normalizar(query)
            send['add']["grupopreguntas"]['preguntas'] = query
            send["get"] = {
                'db': config.db,
                'grupopreguntas':{
                     'ID': id,
                     'preguntas': query_get
                  }
                }
        if type_query == 'rm':
            send['rm'] = {'db': config.db, self.tbName: query}

        self.data_send['data'] = json.dumps(send)
        self.__httprequest__(self.data_send, on_success)

    def get_model(self, title):
        model = PreguntasModel()
        model.title = title
        return model

    def get_datos_button(self, regs):
        datos = []
        for reg in regs:
            dato = {
                'bgColor': reg['color'],
                'text': reg['nombre'],
                'reg': reg
            }
            datos.append(dato)
        return datos
