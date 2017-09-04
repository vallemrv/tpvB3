# @Author: Manuel Rodriguez <valle>
# @Date:   02-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 04-Sep-2017
# @License: Apache license vesion 2.0

import config

from models import *
from kivy.storage.jsonstore import JsonStore


db = JsonStore("../db/clases.json")
for c in db['db'].get('lista'):
    print c
    cl = Clases(nombre=c["text"], color=c["color"], orden=0)
    cl.save()
    pdb = JsonStore("../"+c["productos"])
    for p in pdb['db'].get('lista'):
        print p
        prl = Productos(nombre=p["text"], color=p["color"],
                        precio=p["precio"])
        cl.productos.add(prl)
