# @Author: Manuel Rodriguez <valle>
# @Date:   18-Feb-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 18-Feb-2018
# @License: Apache license vesion 2.0


import config
import importlib

module = importlib.import_module("models.db")
for k, v in module.__dict__.items():
    if type(v) == type:
        v()
