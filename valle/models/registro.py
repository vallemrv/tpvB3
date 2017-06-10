# -*- coding: utf-8 -*-
"""Programa Gestion para el TPV del Btres

    Autor: Manuel Rodriguez
    Licencia: Apache v2.0

"""
import sqlite3
import json
from campos import Campo
from relationship import RelationShip


class Registro(object):
    tableName = "secciones"
    version = 0
    dbName = "valle_orm.db"
    ID = -1
    lstCampos = []
    foreingKey = []

    def __init__(self, **kargs):
        if "tableName" in kargs:
            self.tableName = kargs["tableName"]
        else:
            self.tableName = self.__class__.__name__.lower()
        self.__convertir_campos__()
        self.__crearDb__()

    def __convertir_campos__(self):
        for key in dir(self):
            tipo = type(getattr(self, key))
            if tipo is Campo:
                self.lstCampos.append(key)
            elif tipo is RelationShip:
                relation = getattr(self, key)
                relation.reg = self
                if relation.tipo == "ONE":
                    frgKey= "FOREIGN KEY({0}) REFERENCES {1}(ID)".format(relation.relacion,
                                                                         relation.tableName)
                    setattr(self, relation.relacion,
                            Campo(dato=-1, tipo="INTEGER"))
                    self.foreingKey.append(frgKey)
                    self.lstCampos.append(str(relation.relacion))



    def __crearDb__(self):
        if self.tableName != "registro":
            fields = ["ID INTEGER PRIMARY KEY AUTOINCREMENT"]
            for key in self.lstCampos:
                fields.append("{0} {1}".format(key,
                                               getattr(self,
                                                       key).getTipoDatos()))
            frgKey = "" if len(self.foreingKey)==0 else ", {0} {1}".format(", ".join(self.foreingKey),
                                                                          "ON DELETE CASCADE")


            values = ", ".join(fields)
            sql = "CREATE TABLE IF NOT EXISTS {1} ({0}{2}) ;".format(values,
                                                                self.tableName,
                                                                frgKey)

            db = sqlite3.connect(self.dbName)
            cursor= db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(sql)
            db.commit()
            db.close()



    def save(self):
        if type(self) is Registro: self.__convertir_campos__()
        if self.ID == -1:
            keys =[]
            vals = []
            for key in self.lstCampos:
                val = getattr(self, key)
                keys.append(key)
                vals.append(str(val.pack()))
            cols = ", ".join(keys)
            values = ", ".join(vals)
            sql = "INSERT INTO {0} ({1}) VALUES ({2});".format(self.tableName,
                                                               cols, values);
        else:
            vals = []
            for key in self.lstCampos:
                val = getattr(self, key)
                vals.append("{0} = {1}".format(key, val.pack()))
            values = ", ".join(vals)
            sql = "UPDATE {0}  SET {1} WHERE ID={2};".format(self.tableName,
                                                             values, self.ID);
        db = sqlite3.connect(self.dbName)
        cursor= db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(sql)
        if self.ID == -1:
            self.ID = cursor.lastrowid
        db.commit()
        db.close()

    def remove(self):
        sql = "DELETE FROM {0} WHERE ID={1};".format(self.tableName,
                                                     self.ID);

        db = sqlite3.connect(self.dbName)
        cursor= db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(sql)
        db.commit()
        db.close()
        self.ID = -1

    def getAll(self, order=None, query=None, limit=None, offset=None):
        order = "" if not order else "ORDER BY %s" % unicode(order)
        query = "" if not query else "WHERE %s" % unicode(query)
        limit = "" if not limit else "LIMIT %s" % limit
        offset = "" if not offset else "OFFSET %s" % offset
        sql = "SELECT * FROM {0} {1} {2} {3} {4};".format(self.tableName, order, query,
                                              limit, offset)

        db = sqlite3.connect(self.dbName)
        cursor= db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(sql)
        reg = cursor.fetchall()
        d = cursor.description
        db.commit()
        db.close()
        registros = []

        for r in reg:
            res = dict({k[0]: v for k, v in list(zip(d, r))})
            obj = self.__class__()
            for k, v in res.items():
                if k == "ID":
                    obj.ID = v
                else:
                    setattr(obj, k, Campo(dato=v))

            registros.append(obj)

        return registros

    def find(self, query, order=None, limit=None, offset=None):
        order = "" if not order else "ORDER BY %s" % order
        limit = "" if not limit else "LIMIT %s" % limit
        offset = "" if not offset else "OFFSET %s" % offset
        sql = "SELECT * FROM {0} WHERE {1} {2} {3} {4};".format(self.tableName,
                                                        unicode(query),
                                                        order, limit, offset)
        db = sqlite3.connect(self.dbName)
        cursor= db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(sql)
        reg = cursor.fetchall()
        d = cursor.description
        db.commit()
        db.close()
        registros = []

        for r in reg:
            res = dict({k[0]: v for k, v in list(zip(d, r))})
            obj = self.__class__()
            for k, v in res.items():
                if k=="ID":
                    obj.ID = v
                else:
                    setattr(obj, k, Campo(dato=v))

            registros.append(obj)

        return registros

    def join(self,  relacion, table, colunm=None, query=None, order=None , limit=None, offset=None):
        order = "" if not order else "ORDER BY %s" % order
        query = "" if not query else "WHERE %s" % unicode(query)
        colunm = "*" if not colunm else ", ".join(colunm)
        limit = "" if not limit else "LIMIT %s" % limit
        offset = "" if not offset else "OFFSET %s" % offset
        sql = "SELECT {5} FROM {0} INNER JOIN {3} ON {4} {1} {2};".format(self.tableName,
                                                                query,
                                                                order, table,
                                                                relacion,
                                                                colunm)
        db = sqlite3.connect(self.dbName)
        cursor= db.cursor()
        cursor.execute(sql)
        reg = cursor.fetchall()
        d = cursor.description
        db.commit()
        db.close()
        registros = []

        for r in reg:
            res = dict({k[0]: v for k, v in list(zip(d, r))})
            obj = Registro(tableName=self.tableName)

            for k, v in res.items():
                if k=="ID":
                    obj.ID = v
                else:
                    setattr(obj, k, Campo(dato=v))

            registros.append(obj)

        return registros

    def select(self, query):
        registros = []

        if sqlite3.complete_statement(unicode(query)):
            db = sqlite3.connect(self.dbName)
            cursor= db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(query)
            reg = cursor.fetchall()
            d = cursor.description
            db.commit()
            db.close()

            for r in reg:
                res = dict({k[0]: v for k, v in list(zip(d, r))})
                obj = Registro(tableName=self.tableName)
                for k, v in res.items():
                    if k=="ID":
                        obj.ID = v
                    else:
                        setattr(obj, k, Campo(dato=v))

                registros.append(obj)

        return registros

    def execute(self, query):
        if sqlite3.complete_statement(query):
            db = sqlite3.connect(self.dbName)
            cursor= db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(query)
            db.commit()
            db.close()

    def getPk(self, idr):
        sql = "SELECT * FROM {0} WHERE ID={1};".format(self.tableName, idr)
        db = sqlite3.connect(self.dbName)
        cursor= db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(sql)
        reg = cursor.fetchone()
        d = cursor.description
        db.commit()
        db.close()
        if reg:
            res = dict({k[0]: v for k, v in list(zip(d, reg))})
            for k, v in res.items():
                if k=="ID":
                    self.ID = v
                else:
                    setattr(self, k, Campo(dato=v))

    def toJSON(self):
        if type(self) is Registro: self.__convertir_campos__()
        js = {"ID": self.ID}
        for key in self.lstCampos:
            js[key] = getattr(self, key).get()

        return json.dumps(js)

    def toDICT(self):
        if type(self) is Registro: self.__convertir_campos__()
        js = {"ID": self.ID}
        for key in self.lstCampos:
            js[key] = getattr(self, key).get()

        return js

    def __cargarDatos(self, datos):
        for k, v in datos.items():
            if k=="ID":
                self.ID = v
            else:
                setattr(self, k, Campo(dato=v))


    @staticmethod
    def serialize(registros):
        lista = []
        for r in registros:
            reg = {}
            reg["tableName"] = r.tableName
            reg["datos"] = r.toDICT()
            lista.append(reg)

        return json.dumps(lista)

    @classmethod
    def deSerialize(cls, dbJSON):
        lista = json.loads(dbJSON)
        registros = []
        for l in lista:
            obj = cls()
            obj.tableName = l["tableName"]
            obj.__cargarDatos(l["datos"])
            registros.append(obj)

        return registros
