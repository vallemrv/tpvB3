# -*- coding: utf-8 -*-
#
# @Author: Manuel Rodriguez <valle>
# @Date:   29-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Filename: field.py
# @Last modified by:   valle
# @Last modified time: 16-Mar-2018
# @License: Apache license vesion 2.0

import importlib
import uuid
from .constant import constant
from decimal import *
from datetime import date, datetime
try:
    from exceptions import ValueError
except:
    unicode = lambda s: str(s)



class Field(object):
    def __init__(self, null=False, default=None, unique=False, **options):
        self.tipo_class = constant.TIPO_CAMPO
        self.db_column = None
        self.default = default
        self.null = null
        self.tipo = 'TEXT'
        self.dato = self.default
        self.unique = unique
        for k, v in options.items():
            setattr(self, k, v)


    def get_pack_dato(self, dato=None):
        if dato == None:
            dato = self.get_dato()
            
        if self.null == False and dato == None:
            print(ValueError("No se puden guardar valores nulos"))
            return 'NULL'
        elif self.null == True and dato == None:
            return 'NULL'
        elif self.tipo in  ["TEXT", "VARCHAR"]:
            return u'"{0}"'.format(unicode(dato))
        elif self.tipo is "DATETIME":
            return   u'"{0}"'.format(unicode(dato.strftime("%Y-%m-%d %H:%M:%S.%f")))
        elif self.tipo == "DATE":
            return   u'"{0}"'.format(unicode(dato.strftime("%Y-%m-%d")))
        elif self.tipo == "BOOL":
            return 1 if self.dato == 1 or self.dato == True else 0
        else:
            return dato

    def get_pack_default(self):
        if self.tipo in  ["TEXT", "VARCHAR"]:
            return u'"{0}"'.format(unicode(self.default))
        else:
            return self.default


    def get_dato(self):
        return self.dato

    def set_dato(self, value):
        self.dato = value


    def get_serialize_data(self, key):
        obj_return = self.__dict__
        if self.db_column == None:
            obj_return['db_column'] = key
            self.db_column = key
        return  obj_return

    def getStrTipo(self):
        return self.tipo

    def toQuery(self):
        strnull = "" if self.null == True else ' NOT NULL '
        strdefault = "" if self.default == None else " DEFAULT %s" % self.get_pack_default()
        strunique = "" if self.unique == False else " UNIQUE "
        return u"{0} {1} {2} {3}".format(self.getStrTipo(), strnull, strdefault, strunique)

class CharField(Field):
    def __init__(self, label=None, max_length=None, null=False, default=None, unique=False, **options):
        super(CharField, self).__init__(null=null, default=default, unique=unique, **options)
        self.tipo="VARCHAR"
        self.class_name = "CharField"
        self.max_length=max_length
        self.label = label

    def set_dato(self, value):
        if value != None:
            how_long = len(value)
            if how_long > self.max_length:
                self.dato = value[:self.max_length-how_long]
            else:
                self.dato = value
        else:
            self.dato = value


    def getStrTipo(self):
        return "VARCHAR(%s)" % self.max_length


class AutoField(Field):
    def __init__(self, label=None, primary_key=True, **options):
        options["null"]=True
        options["unique"]=False
        options["default"]=None
        super(AutoField, self).__init__(**options)
        self.tipo="INTEGER"
        self.class_name = "AutoField"
        self.primary_key=primary_key
        self.dato = -1


    def getStrTipo(self):
        str_primary_key = "PRIMARY KEY" if self.primary_key else ""
        return "INTEGER %s AUTOINCREMENT" % str_primary_key


class EmailField(CharField):
    def __init__(self, label=None, max_length=254, null=False, default=None, unique=False, **options):
        super(EmailField, self).__init__(max_length=max_length, null=null, default=default, unique=unique, **options)
        self.class_name = 'EmailField'

    def set_dato(self, value):
        if value != None and value != "" and not ("@" in value and "." in value):
            print(ValueError('Formato email no valido'))

        self.dato = value


class DecimalField(Field):
    def __init__(self, label=None, max_digits=10, decimal_places=2, null=False, default=None, unique=False, **options):
        super(DecimalField, self).__init__(null=null, default=default, unique=unique, **options)
        self.max_digits=max_digits
        self.decimal_places=decimal_places
        self.class_name = "DecimalField"

    def set_dato(self, value):
        if type(value) in (unicode, str):
            self.dato = float(value.replace(",", "."))
        else:
            self.dato = value

    def get_dato(self):
        if type(self.dato) in [float, int]:
            dato = "%."+str(self.decimal_places)+"f"
            dato = dato % self.dato
        return float(dato)


    def getStrTipo(self):
        return u"DECIMAL({0},{1})".format(self.max_digits, self.decimal_places)


class DateField(Field):
    def __init__(self, label=None, auto_now=False, auto_now_add=True, null=False, default=None, unique=False, **options):
        super(DateField, self).__init__(null=null, default=default, unique=unique, **options)
        self.tipo="DATE"
        self.class_name = "DateField"
        self.auto_now=auto_now
        self.auto_now_add=auto_now_add


    def get_dato(self):
        if self.auto_now:
            self.dato = date.today()
        elif self.auto_now_add and self.dato == None:
            self.dato = date.today()
        return self.dato

    def set_dato(self, value):
        if type(value) == date:
            self.dato = date
        else:
            fecha_split = value.split("-")
            self.dato = date(int(fecha_split[0]), int(fecha_split[1]), int(fecha_split[2]))



class DateTimeField(Field):
    def __init__(self, label=None, auto_now=False, auto_now_add=False, null=False, default=None, unique=False, **options):
        super(DateTimeField, self).__init__(null=null, default=default, unique=unique, **options)
        self.tipo="DATETIME"
        self.class_name = "DateTimeField"
        self.auto_now = auto_now
        self.auto_now_add=auto_now_add

    def get_dato(self):
        if self.auto_now:
            self.dato = datetime.now()
        elif self.auto_now_add and self.dato == None:
            self.dato = datetime.now()
        return self.dato

    def set_dato(self, value):
        if type(value) == datetime:
            self.dato = value
        else:
            try:
                self.dato = datetime.strptime(value.replace("T", " "),"%Y-%m-%d %H:%M:%S.%f")
            except:
                self.dato = datetime.strptime(value.replace("T", " "),"%Y-%m-%d %H:%M:%S")


class BooleanField(Field):
    def __init__(self, **options):
        super(BooleanField, self).__init__(**options)
        self.tipo="BOOL"
        self.class_name = "BooleanField"

    def get_dato(self):
        return True if self.dato == 1 or self.dato == True else False

    def set_dato(self, value):
        self.dato = True if value == True or value == 1 else False



class IntegerField(Field):
    def __init__(self, label=None, null=False, default=None, unique=False, **options):
        super(IntegerField, self).__init__(null=null, default=default, unique=unique, **options)
        self.tipo="INTEGER"
        self.class_name = "IntegerField"


class FloatField(Field):
    def __init__(self, label=None, null=False, default=None, unique=False, **options):
        super(FloatField, self).__init__(null=null, default=default, unique=unique, **options)
        self.tipo="REAL"
        self.class_name = "FloatField"


class TextField(Field):
    def __init__(self, label=None, null=False, default=None, unique=False, **options):
        super(TextField, self).__init__(null=null, default=default, unique=unique, **options)
        self.tipo="TEXT"
        self.class_name = "TextField"


class UUIDField(Field):
    def __init__(self, **options):
        super(UUIDField, self).__init__(null=False, default=default, unique=True, **options)
        self.class_name = "UUIDField"
        self.tipo="TEXT"
        self.unique = True

    def get_dato(self):
        return str(uuid.uuid4())
