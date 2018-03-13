# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <vallemrv>
# @Date:   29-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 18-Feb-2018
# @License: Apache license vesion 2.0

import sys
import inspect
import importlib
from constant import constant

class RelationShip(object):

    def __init__(self, othermodel, **options):
        self.tipo_class = constant.TIPO_RELATION
        self.class_name = "ForeignKey"
        self.main_module = None
        self.related_class = None
        self.main_class = None
        self.field_related_name = None
        self.field_related_id = None
        self.on_delete = constant.CASCADE
        if type(othermodel) in (str, unicode):
            self.related_name = othermodel
        else:
            self.related_name = othermodel.__name__
            self.related_class = othermodel

        for k, v in options.items():
            setattr(self, k, v)


    def get_id_field_name(self):
        if self.field_related_name == None:
            return self.related_name.lower() + "_id"
        return self.field_related_name

    def set_id_field_name(self, value):
        self.field_related_name = value

    def get(self, **condition):
        pass

    field_name_id = property(get_id_field_name, set_id_field_name)

class OneToManyField(RelationShip):
    def __init__(self, main_class, related_name, **kargs):
        super(OneToManyField, self).__init__(related_name, **kargs)
        self.class_name = "OneToManyField"
        self.main_class = main_class
        self.related_name = related_name
        if self.main_module == None:
            self.main_module = self.main_class.__module__
        self.related_class = create_class_related(self.main_module, self.related_name)
        self.tb_name_main = self.main_class.get_db_table()
        if self.field_related_id == None:
            self.field_name_id = self.tb_name_main + "_id"



    def get(self, **condition):
        query = u"{0}={1}".format(self.field_name_id, self.main_class.id)

        if 'query' in condition:
            condition['query'] += " AND " + query
        else:
            condition['query'] = query

        return self.related_class.filter(**condition)


    def add(self, child):
        if self.main_class.id == -1:
            self.main_class.save()
        setattr(child, self.field_name_id, self.main_class.id)
        child.save()



class ForeignKey(RelationShip):
    def __init__(self, othermodel, on_delete=constant.CASCADE, **kargs):
        super(ForeignKey, self).__init__(othermodel, **kargs)
        self.class_name = "ForeignKey"
        self.on_delete = on_delete


    def get_choices(self, **condition):
        return self.related_class.getAll(**condition)

    def get_sql_pk(self):
        sql = u"FOREIGN KEY({0}) REFERENCES {1}(id) %s" % self.on_delete
        sql = sql.format(self.field_name_id, self.related_name)
        return sql

    def get(self):
        if self.related_class == None:
            if self.main_module == None:
                self.main_module = self.main_class.__module__

            self.related_class = create_class_related(self.main_module, self.related_name)

        reg = self.related_class(db_name=self.main_class.db_name)
        reg.load_by_pk(getattr(self.main_class, self.field_name_id))
        return reg

class ManyToManyField(RelationShip):

    def __init__(self, othermodel, db_table_nexo=None,  **kargs):
        super(ManyToManyField, self).__init__(othermodel, **kargs)
        self.class_name = "ManyToManyField"
        self.db_table_nexo = db_table_nexo


        if self.main_class != None:
            if self.main_module == None:
                self.main_module = self.main_class.__module__

            self.tb_name_main = self.main_class.get_db_table()
            self.related_class = create_class_related(self.main_module, self.related_name)
            self.tb_name_related = self.related_class.get_db_table()
            if self.field_related_id == None:
                self.field_name_id = self.tb_name_main + "_id"
                self.field_related_id = self.tb_name_related + "_id"


    def get_sql_tb_nexo(self):
        key = "PRIMARY KEY ({0}, {1})".format(self.field_name_id, self.field_related_id)
        frgKey = u"FOREIGN KEY({0}) REFERENCES {1}(id) ON DELETE CASCADE, "
        frgKey = frgKey.format(self.field_name_id, self.tb_name_main)
        frgKey += u"FOREIGN KEY({0}) REFERENCES {1}(id) ON DELETE CASCADE"
        frgKey = frgKey.format(self.field_related_id, self.tb_name_related)
        sql = u"CREATE TABLE IF NOT EXISTS {0} ({1}, {2} ,{3}, {4});"
        sql = sql.format(self.db_table_nexo, self.field_name_id+" INTEGER NOT NULL",
                         self.field_related_id+" INTEGER NOT NULL ",key, frgKey)


        return sql


    def get(self,  **condition):
        if "tb_nexo" in condition:
            self.db_table_nexo = condition["tb_nexo"]
        if "field_related_id" in condition:
            self.field_related_id = condition["field_related_id"]
        if "field_name_id" in condition:
            self.field_name_id = condition["field_name_id"]

        condition["columns"] = [self.tb_name_related+".*"]

        condition["joins"] = [(self.db_table_nexo + " ON "+ \
                             self.db_table_nexo+"."+self.field_related_id+\
                             "="+self.tb_name_related+".id")]
        query = self.field_name_id+"="+str(self.main_class.id)
        if 'query' in condition:
            condition["query"] += " AND " + query
        else:
            condition["query"] = query

        if self.related_class == None:
            if self.main_module == None:
                self.main_module = self.main_class.__module__

            self.related_class = create_class_related(self.main_module, self.related_name)

        return self.related_class.filter(**condition)


    def add(self, *childs):
        for child in childs:
            child.save()
            cols = [self.field_name_id, self.field_related_id]
            values = [str(self.main_class.id), str(child.id)]
            sql = u"INSERT OR REPLACE INTO {0} ({1}) VALUES ({2});".format(self.db_table_nexo,
                                                               ", ".join(cols), ", ".join(values));
            self.main_class.execute(sql)

    def delete(self, child):
        sql = u"DELETE FROM {0} WHERE {1}={2}  AND {3}={4};".format(self.db_table_nexo,
                                                                    self.field_name_id,
                                                                    child.id,
                                                                    self.field_related_id,
                                                                    self.main_class.id)
        self.main_class.execute(sql)


class ManyToManyChild(RelationShip):

    def __init__(self, main_class, related_name,  **kargs):
        super(ManyToManyChild, self).__init__(related_name, **kargs)
        self.class_name = "ManyToManyChild"
        self.main_class = main_class
        self.related_name = related_name
        if self.main_module == None:
            self.main_module = self.main_class.__module__

        self.related_class = create_class_related(self.main_module, self.related_name)
        self.tb_name_main = self.main_class.get_db_table()
        self.tb_name_related = self.related_class.get_db_table()
        self.db_table_nexo = self.tb_name_related  + '_' + self.tb_name_main
        if self.field_related_id == None:
            self.field_name_id = self.tb_name_main + "_id"
            self.field_related_id = self.tb_name_related + "_id"


    def get(self,  **condition):
        if "tb_nexo" in condition:
            self.db_table_nexo = condition["tb_nexo"]
        if "field_related_id" in condition:
            self.field_related_id = condition["field_related_id"]
        if "field_name_id" in condition:
            self.field_name_id = condition["field_name_id"]

        condition["columns"] = [self.tb_name_related+".*"]

        condition["joins"] = [(self.db_table_nexo + " ON "+ \
                             self.db_table_nexo+"."+self.field_related_id+\
                             "="+self.tb_name_related+".id")]
        query = self.field_name_id+"="+str(self.main_class.id)
        if 'query' in condition:
            condition["query"] += " AND " + query
        else:
            condition["query"] = query

        return self.related_class.filter(**condition)


    def add(self, *childs):
        for child in childs:
            child.save()
            cols = [self.field_name_id, self.field_related_id]
            values = [str(self.main_class.id), str(child.id)]
            sql = u"INSERT OR REPLACE INTO {0} ({1}) VALUES ({2});".format(self.db_table_nexo,
                                                               ", ".join(cols), ", ".join(values));
            self.main_class.execute(sql)

    def delete(self, child):
        sql = u"DELETE FROM {0} WHERE {1}={2}  AND {3}={4};".format(self.db_table_nexo,
                                                                    self.field_related_id,
                                                                    child.id,
                                                                    self.field_name_id,
                                                                    self.main_class.id)

        self.main_class.execute(sql)


def create_class_related(module, class_name):
    module = ".".join(module.split(".")[:-1])
    modulo = importlib.import_module(module)
    nclass = getattr(modulo,  str(class_name))
    return nclass
