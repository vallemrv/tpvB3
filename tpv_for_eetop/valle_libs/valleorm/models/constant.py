# @Author: Manuel Rodriguez <vallemrv>
# @Date:   29-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 21-Dec-2017
# @License: Apache license vesion 2.0

class Constant():
    def __init__(self):
        self.TIPO_CAMPO = "tipo_campo"
        self.TIPO_RELATION = "tipo_relation"
        self.CASCADE = "ON DELETE CASCADE"
        self.SET_NULL = "ON DELETE SET NULL"
        self.SET_DEFAUT = "ON DELETE SET DEFAULT"
        self.NO_ACTION = "ON DELETE NO ACTION"
        

constant = Constant()
