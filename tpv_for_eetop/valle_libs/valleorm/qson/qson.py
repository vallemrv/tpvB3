# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   25-Dec-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 13-Mar-2018
# @License: Apache license vesion 2.0

from kivy.network.urlrequest import UrlRequest
from kivy.core import Logger
import urllib
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
        self.exclude = []
        for k, v in filter.items():
            self.filter[k] = v

    def add_filter(self, **filter):
        for k, v in filter.items():
            self.filter[k] = v

    def add_exclude(self, **filter):
        exclude = {}
        for k, v in filter.items():
            exclude[k] = v
        self.exclude.append(exclude)

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

    def __init__(self, **args):
        self.qson_sender = {}

    def __got_error__(self, req,  *args):
        req._resp_status = "Error"
        Logger.debug("got error {0}".format(req.url))

    def __got_fail__(self, req, *args):
        req._resp_status = "Fail"
        Logger.debug("got fail {0}".format(req.url))

    def __got_redirect__(self, req, *args):
        req._resp_status = "Redirect"
        Logger.debug("got redirect {0}".format(req.url))


    def send(self, on_success, wait=True):

        SEND_DATA = {'data':json.dumps(self.qson_sender)}
        data = urllib.urlencode(SEND_DATA)
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/json'}
        r = UrlRequest(self.url, on_success=on_success, req_body=data,
                       req_headers=headers, method="POST",
                       on_failure=self.__got_fail__,
                       on_error=self.__got_error__,
                       on_redirect=self.__got_redirect__)

        if wait:
            r.wait()



    def send_data(self, on_success, send_data):
        data = urllib.urlencode(send_data)
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/json'}
        r = UrlRequest(self.url, on_success=on_success, req_body=data,
                       req_headers=headers, method="POST",
                       on_failure=self.got_fail,
                       on_error=self.got_error, debug=True,
                       on_redirect=self.got_redirect)

        if wait:
            r.wait()


    def get_data(self):
        SEND_DATA = {'data':json.dumps(self.qson_sender)}
        return SEND_DATA


    def join(self,  *qsons):
        if not "join" in self.qson_sender:
            self.qson_sender["join"] =  {"db": self.db_name,
                                 "rows": []}
        for m in qsons:
            self.qson_sender["join"]["rows"].append(m.get_qson())



    def save(self, *qsons):
        if not "add" in self.qson_sender:
            self.qson_sender["add"] = {"db": self.db_name,
                                "rows": []}
        for m in qsons:
            self.qson_sender["add"]["rows"].append(m.get_qson())




    def filter(self,  *qsons):
        if not "get" in self.qson_sender:
            self.qson_sender['get'] =  {"db": self.db_name,
                                "rows": []}
        for m in qsons:
            self.qson_sender["get"]["rows"].append(m.get_qson())


    def delete(self, *qsons):
        if not "get" in self.qson_sender:
            self.qson_sender["rm"] = {"db": self.db_name,
                               "rows": []}
        for m in qsons:
            self.qson_sender["rm"]["rows"].append(m.get_filter())
