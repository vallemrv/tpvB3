# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <vallemrv>
# @Date:   29-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 26-Feb-2018
# @License: Apache license vesion 2.0

from datetime import date, datetime
import sqlite3
import json
import base64

from .constant import constant
from .fields import *
from .relatedfields import *



class Model(object):
    def __init__(self, db_name="db.sqlite3", **options):
        self.lstCampos = []
        self.foreingKeys = []
        self.db_table = self.__class__.__name__.lower()
        self.db_name = db_name
        self.__crea_tb_relationship__()
        if hasattr(self, 'Meta'):
            meta = getattr(self, 'Meta')
            if hasattr(meta, "db_table"):
                self.db_table = getattr(meta, "db_table")
            if hasattr(meta, "db_name"):
                self.db_name = getattr(meta, "db_name")


        if self.db_table != "model":
            self.__init_campos__()

        for k, v in options.items():
            if k not in self.lstCampos:
                continue
            if k == 'id':
                self.load_by_pk(v)
            setattr(self, k, v)

    def __save_relationship__(self, main_class, relate_class, tipo):
        sql = "SELECT id FROM relationship_db WHERE main_class='%s' AND relate_class='%s';"
        sql = sql % (main_class, relate_class)
        reg = Model.execute_select(sql)
        if len(reg) <= 0:
            sql = u"INSERT OR REPLACE INTO relationship_db (main_class, relate_class, tipo) VALUES ('{0}','{1}', '{2}');"
            sql = sql.format(main_class, relate_class, tipo)
            self.execute(sql)

    def __crea_tb_relationship__(self):
        IDprimary = "ID INTEGER PRIMARY KEY AUTOINCREMENT"
        sql = "CREATE TABLE IF NOT EXISTS relationship_db (%s, main_class TEXT, relate_class TEXT, tipo TEXT);"
        sql = sql % IDprimary
        self.execute(sql)

    def __get_relationship__(self):
        sql = "SELECT * FROM relationship_db WHERE main_class='%s'" % self.__class__.__name__
        return Model.execute_select(sql)


    def __unicode__(self):
        return  unicode(self)


    def __setattr__(self, attr, value):
        es_dato_simple = type(value) in (str, int, bool, float, unicode, date, datetime)
        es_dato_simple = es_dato_simple and hasattr(self, 'lstCampos') and attr in self.lstCampos
        if es_dato_simple or value == None:
            field = super(Model, self).__getattribute__(attr)
            field.set_dato(value)
        else:
            super(Model, self).__setattr__(attr, value)


    def __getattribute__(self, attr):
        value = super(Model, self).__getattribute__(attr)
        if hasattr(value, 'tipo_class') and value.tipo_class == constant.TIPO_CAMPO:
            return value.get_dato()

        return value


    #Introspection of the inherited class
    def __init_campos__(self):
        for key in dir(self):
            field =  super(Model, self).__getattribute__(key)
            tipo_class = ""
            if hasattr(field, 'tipo_class'):
                tipo_class = field.tipo_class
            if tipo_class == constant.TIPO_CAMPO:
                setattr(self, key, field.__class__(**field.get_serialize_data(key)))
                self.lstCampos.append(key)
            elif tipo_class == constant.TIPO_RELATION:
                setattr(self, key, field.__class__(othermodel=field.related_name,
                                                   on_delete=field.on_delete,
                                                   main_class=self,
                                                   field_related_name=field.field_related_name,
                                                   field_related_id=field.field_related_id))

                self.__save_relationship__(field.related_name, self.__class__.__name__, field.class_name)


                if field.class_name in "ForeignKey":
                    setattr(self, field.field_name_id, IntegerField(db_column=field.field_name_id))
                    self.lstCampos.append(field.field_name_id)
                    self.foreingKeys.append(field.get_sql_pk())

                if field.class_name == "ManyToManyField":
                    rel = getattr(self, key)
                    rel.db_table_nexo = field.db_table_nexo
                    if rel.db_table_nexo != None:
                        exists = Model.exists_table(rel.db_table_nexo, db_name=self.db_name)
                        if not exists:
                            self.__crear_tb_nexo__(rel)
                    else:
                        table_nexo = self.__find_db_nexo__(rel.tb_name_main, rel.tb_name_related)
                        if table_nexo == None:
                            rel.db_table_nexo = rel.tb_name_main + '_' + rel.tb_name_related
                            self.__crear_tb_nexo__(rel)
                        else:
                            rel.db_table_nexo = table_nexo


        if 'id' not in self.lstCampos:
            self.id = AutoField(primary_key=True, db_column='id')
            self.lstCampos.append("id")

        self.__create_if_not_exists__()
        self.__crear_relationship__()


    def __crear_relationship__(self):
        rel = self.__get_relationship__()
        for r in rel:
            if r["tipo"] == "ForeignKey":
                setattr(self, r["relate_class"].lower()+"_set",
                        OneToManyField(self, r["relate_class"]))
            elif r["tipo"] == "ManyToManyField":
                setattr(self, r["relate_class"].lower()+"_set",
                        ManyToManyChild(self, r["relate_class"]))



    def __find_db_nexo__(self, tb1, tb2):
        db = sqlite3.connect(self.db_name)
        cursor= db.cursor()
        condition = u" AND (name='{0}' OR name='{1}')".format(tb1+"_"+tb2, tb2+"_"+tb1)
        sql = u"SELECT name FROM sqlite_master WHERE type='table' %s;" % condition
        cursor.execute(sql)
        reg = cursor.fetchone()
        db.commit()
        db.close()
        if reg:
            find = True
            return reg[0]
        return None


    def __create_if_not_exists__(self):
        fields = []
        for key in self.lstCampos:
            field  = super(Model, self).__getattribute__(key)
            fields.append(u"'{0}' {1}".format(field.db_column, field.toQuery()))

        frgKey = "" if len(self.foreingKeys)==0 else u", {0}".format(", ".join(self.foreingKeys))

        values = ", ".join(fields)
        sql = u"CREATE TABLE IF NOT EXISTS {1} ({0}{2});".format(values,
                                                            self.db_table,
                                                            frgKey)

        self.execute(sql)

    def __crear_tb_nexo__(self, relation):
        sql = relation.get_sql_tb_nexo()
        self.execute(sql)


    def __cargar_datos__(self, **datos):
        for k, v in datos.items():
            if k not in self.lstCampos:
                raise AttributeError("El atributo %s no esta en el modelo"% k)
            setattr(self, k, v)


    def save(self, **kargs):
        self.__cargar_datos__(**kargs)
        self.id = -1 if self.id == None else self.id

        keys =[]
        vals = []
        for key in self.lstCampos:
            val = super(Model, self).__getattribute__(key)
            if key != 'id' or (key == 'id' and self.id > 0):
                keys.append(val.db_column)
                vals.append(str(val.get_pack_dato()))


        cols = ", ".join(keys)
        values = ", ".join(vals)
        sql = u"INSERT OR REPLACE INTO {0} ({1}) VALUES ({2});".format(self.db_table,
                                                           cols, values);
        db = sqlite3.connect(self.db_name)
        cursor= db.cursor()
        cursor.execute(sql)
        if self.id == -1:
            self.id = cursor.lastrowid
        db.commit()
        db.close()

    def delete(self):
        self.id = -1 if self.id == None else self.id
        sql = u"DELETE FROM {0} WHERE id={1};".format(self.db_table, self.id)
        self.execute(sql)
        self.id = -1


    def empty(self):
        self.id = -1;
        self.execute("DELETE FROM %s;" % self.db_table)


    def execute(self, query):
        if sqlite3.complete_statement(query):
            db = sqlite3.connect(self.db_name)
            cursor= db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(query)
            db.commit()
            db.close()

    def pack_dato(self, dato):
        if type(dato) in [int, float]:
            return  dato
        else:
            return "'%s'" % dato

    def load_by_pk(self, pk):
        sql = u"SELECT * FROM {0} WHERE id={1};".format(self.db_table, pk)
        db = sqlite3.connect(self.db_name)
        cursor= db.cursor()
        cursor.execute(sql)
        reg = cursor.fetchone()
        d = cursor.description
        db.commit()
        db.close()
        if reg:
            res = dict({k[0]: v for k, v in list(zip(d, reg))})
            self.__cargar_datos__(**res)

    def toJSON(self):
        js = self.toDICT()
        return json.dumps(js, ensure_ascii=False)

    def toDICT(self):
        from datetime import date, datetime
        js = {}
        for key in self.lstCampos:
            if not (key == "id" and self.id < 1):
                v =  getattr(self, key)
                if not (v == None or v == "NULL"):
                    if type(v) == date:
                        js[key] = v.strftime("%Y-%m-%d")
                    elif type(v) == datetime:
                        js[key] = v.strftime("%Y-%m-%d %H:%M:%S.%f")
                    else:
                        js[key] = v
        return js

    @classmethod
    def empty(cls, db_name="db.sqlite3"):
        sql = "DELETE FROM %s;" % cls.__name__.lower()
        db = sqlite3.connect(self.db_name)
        cursor= db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(sql)
        db.commit()
        db.close()

    @classmethod
    def select(cls, sql, db_name="db.sqlite3"):
        db = sqlite3.connect(db_name)
        cursor= db.cursor()
        cursor.execute(sql)
        reg = cursor.fetchall()
        d = cursor.description
        db.commit()
        db.close()
        registros = []

        for r in reg:
            res = dict({k[0]: v for k, v in list(zip(d, r))})
            obj = cls(db_name=db_name, **res)
            registros.append(obj)

        return registros

    @classmethod
    def get_db_table(cls):
        db_table = cls.__name__.lower()
        if hasattr(cls, 'Meta'):
            meta = getattr(cls, 'Meta')
            if hasattr(meta, "db_table"):
                self.db_table = getattr(meta, "db_table")
        return db_table


    @classmethod
    def filter(cls, db_name="db.sqlite3", **condition):
        db_table = cls.__name__.lower()
        ordering = None
        if hasattr(cls, 'Meta'):
            meta = getattr(cls, 'Meta')
            if hasattr(meta, "db_table"):
                db_table = getattr(meta, "db_table")
            if hasattr(meta, "db_name"):
                db_name = getattr(meta, "db_name")
            if hasattr(meta, "ordering"):
                ord = getattr(meta, "ordering")
                ord_aux = []
                for o in ord:
                    if "-" in o:
                        ord_aux.append(o[1:]+" DESC")
                    else:
                        ord_aux.append(o.replace("+",""))
                ordering = ", ".join(ord_aux)

        columns = "*"
        order, query, limit,  offset, joins, group = ("", )*6
        obj = cls();
        for k, v in condition.items():
            if hasattr(obj, k):
                if query == "":
                    query = "WHERE %s=%s" % (k, obj.pack_dato(v))
                else:
                    query += " AND %s=%s" % (k, val.pack_dato(v))
            if k == 'columns':
                columns = ", ".join(v)
            elif k == 'order':
                order = "ORDER BY %s" % unicode(v)
            elif k =='query':
                query =  "WHERE %s" % unicode(v)
            elif k == 'limit':
                limit = "LIMIT %s" % v
            elif k == 'offset':
                offset = "OFFSET %s" % v
            elif k == 'joins':
                joins = cls.getenerate_joins(v)
            elif k == 'group':
                group = "GROUP BY %s" % v

        if ordering != None:
            if order != '':
                order += ", "+ordering
            else:
                order = "ORDER BY %s" % unicode(ordering)



        sql = u"SELECT {0} FROM {1} {2} {3} {4} {5} {6} {7};".format(columns, db_table,
                                                         joins, query, order, group, limit, offset)

        return cls.select(sql, db_name)

    @staticmethod
    def execute_select(sql, db_name="db.sqlite3"):
        db = sqlite3.connect(db_name)
        cursor= db.cursor()
        cursor.execute(sql)
        reg = cursor.fetchall()
        d = cursor.description
        db.commit()
        db.close()
        registros = []

        for r in reg:
            res = dict({k[0]: v for k, v in list(zip(d, r))})
            registros.append(res)

        return registros

    @staticmethod
    def getenerate_joins(joins):
        strJoins = []
        for j in joins:
            sql = j if j.startswith("INNER") else "INNER JOIN "+j
            strJoins.append(sql)

        return "" if len(strJoins) <=0 else ", ".join(strJoins)

    @staticmethod
    def to_array_dict(registros):
        lista = []
        for r in registros:
            reg = r.toDICT()
            lista.append(reg)

        return lista

    @staticmethod
    def remove_rows(registros):
        lista = []
        for r in registros:
            lista.append({'id': r.id, 'success': True})
            r.remove()
        return lista

    @staticmethod
    def serialize(registros):
        lista = []
        for r in registros:
            reg = {}
            reg["db_table"] = r.db_table
            reg["db_name"] = r.db_name
            reg["datos"] = r.toDICT()
            lista.append(reg)

        return json.dumps(lista)

    @staticmethod
    def deserialize(dbJSON):
        lista = json.loads(dbJSON)
        registros = []
        for l in lista:
            obj = Model(db_table=l["db_table"], db_name=l["db_name"])
            obj.__cargar_datos__(**l["datos"])
            registros.append(obj)

        return registros

    @staticmethod
    def drop_db(db_name='db.sqlite3'):
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE '%sqlite%';"
        db = sqlite3.connect(db_name)
        cursor= db.cursor()
        cursor.execute(sql)
        reg = cursor.fetchall()
        for r in reg:
            cursor.execute("DROP TABLE %s" % r)
        db.commit()
        db.close()

    @staticmethod
    def exists_table(db_table, db_name='db.sqlite3'):
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='%s';"
        sql = sql % db_table
        db = sqlite3.connect(db_name)
        cursor= db.cursor()
        cursor.execute(sql)
        reg = cursor.fetchone()
        db.commit()
        db.close()
        return reg != None


    @staticmethod
    def alter_constraint(db_table, colum_name, parent, db_name='db.sqlite3', on_delete=constant.CASCADE):
        sql = u"ALTER TABLE {0} ADD COLUMN {1} INTEGER REFERENCES {2}(id) {3};"
        sql = sql.format(db_table, colum_name, parent, delete)
        db = sqlite3.connect(db_name)
        cursor= db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()

    @staticmethod
    def alter(field, db_name='db.sqlite3'):
        sql = u"ALTER TABLE {0} ADD COLUMN {1} {2};"
        sql = sql.format(field.db_table, field.field_name, field.toQuery())
        db = sqlite3.connect(db_name)
        cursor= db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()
