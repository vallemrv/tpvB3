# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   25-Dec-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 27-Feb-2018
# @License: Apache license vesion 2.0

from kivy.network.urlrequest import UrlRequest

try:
    unicode("test")
    import urllib
except:
    from urllib3 import request as urllib
import copy
import json

class QSon:
    def __init__(self, db_table,  reg=None, field_name=None,  **filter):
        self.db_table = db_table
        self.childs = []
        if field_name != None:
            self.relation_field = field_name
        if reg != None:
            self.reg = reg
        self.filter = {}
        self.exclude = {}
        for k, v in filter.items():
            self.filter[k] = v

    def add_filter(**filter):
        for k, v in filter.items():
            self.filter[k] = v

    def add_exclude(**filter):
        for k, v in filter.items():
            self.exclude[k] = v

    def append_child(self, qson):
        if not hasattr(qson, 'field_name'):
            qson.relation_field = qson.db_table.lower()
        self.childs.append(qson)


    def get_qson(self):
        obj = copy.deepcopy(self.__dict__)
        obj["childs"]  = []
        for c in self.childs:
            obj["childs"].append(c.get_qson())
        return obj



class QSonSender:
    db_name = None
    url = None
    token = None

    def save(self, on_success,  qson=[], wait=True):
        qson_add = {"add": {"db": self.db_name,
                            "rows": []}}

        for m in qson:
            qson_add["add"]["rows"].append(m.get_qson())

        SEND_DATA = {'data':json.dumps(qson_add)}

        data = urllib.urlencode(SEND_DATA)
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/json'}
        r = UrlRequest(self.url, on_success=on_success, req_body=data,
                       req_headers=headers, method="POST")
        if wait:
            r.wait()

    def all(self, on_success, models=[], wait=True):
        qson_add = {"get": {"db": self.db_name,
                            "tipo": "all",
                            "rows": []}}

        for m in models:
            qson_add["get"]["rows"].append({"db_table":m})

        SEND_DATA = {'data':json.dumps(qson_add)}

        data = urllib.urlencode(SEND_DATA)
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/json'}
        r = UrlRequest(self.url, on_success=on_success, req_body=data,
                       req_headers=headers, method="POST")
        if wait:
            r.wait()

    def filter(self, on_success, qson=(), wait=False):
        qson_add = {"get": {"db": self.db_name,
                            "tipo": "filter",
                            "rows": []}}

        for m in qson:
            qson_add["get"]["rows"].append(m.get_qson())

        SEND_DATA = {'data':json.dumps(qson_add)}
        data = urllib.urlencode(SEND_DATA)
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/json'}
        r = UrlRequest(self.url, on_success=on_success, req_body=data,
                       req_headers=headers, method="POST")
        if wait:
            r.wait()

    def delete(self, on_success, qsonqh=(), wait=False):
        qson_add = {"rm": {"db": self.db_name,
                           "tipo": "filter",
                           "rows": []}}

        for m in qsonqh:
            qson_add["rm"]["rows"].append(m.get_filter())

        SEND_DATA = {'data':json.dumps(qson_add)}

        data = urllib.urlencode(SEND_DATA)
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/json'}
        r = UrlRequest(self.url, on_success=on_success, req_body=data,
                       req_headers=headers, method="POST")
        if wait:
            r.wait()
