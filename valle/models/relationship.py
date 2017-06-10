# -*- coding: utf-8 -*-

"""Programa Gestion para el TPV del Btres

    Autor: Manuel Rodriguez
    Licencia: Apache v2.0

"""


class ManyToMany(object):
    def __init__(self, tbChild, tbNexo, relacion):
        self.tbChild = tbChild
        self.tbNexo = tbNexo
        self.relacion = relacion

class RelationShip(object):
    tipo = "ONE"
    tableName=""
    relacion = ""
    clase = None
    reg = None
    manytoMany = None
    def __init__(self, **kargs):
        if "tipo" in kargs:
            self.tipo = kargs["tipo"]
        if "tableName" in kargs:
            self.tableName = kargs["tableName"]
        if "clase" in kargs:
            self.clase = kargs["clase"]
        if "reg" in kargs:
            self.reg = kargs["reg"]
        if "manytoMany" in kargs:
            self.manytoMany = kargs["tipo"]
        if "relacion" in kargs:
            self.relacion = kargs["relacion"]

    def add(self, child):
        if self.tipo == "MANY":
            getattr(child, self.relacion).set(self.reg.ID)
            child.save()

    def get(self, order=None, query=None):
        if self.tipo == "MANY":
            db = self.clase()
            query = "" if not query else "AND %s" % query
            return db.find(query="{0}={1} {2} ".format(self.relacion,
                                                       self.reg.ID, query),
                           order=order)
        elif self.tipo == "ONE" and self.tableName!="":
            from registro import Registro
            parent = Registro(tableName=self.tableName)
            parent.getPk(getattr(self.reg, self.relacion).get())
            return parent

        elif self.tipo == "MANYTOMANY" and self.manyToMany:
            from registro import Registro
            db = Registro(tableName=self.manytoMany.tbChild)
            query = "" if not query else "WHERE %s" % query
            order = "" if not order else "ORDER BY %s" % order
            tbChild = self.manytoMany.tbChild
            tbNexo = self.manytoMany.tbNexo
            relacion = self.manytoMany.relacion
            sql = '''SELECT {0}.* FROM {1} INNER JOIN {2}
                     ON {1}.ID={2}.{4} INNER JOIN {0}
                     ON {0}.ID={2}.{3} {5} {6}
                     ;'''.format(tbChild, self.tableName,
                                tbNexo, relacion, self.relacion, query,
                                orden)
            return db.select(sql)
