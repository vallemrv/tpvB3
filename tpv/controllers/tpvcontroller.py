# @Author: Manuel Rodriguez <valle>
# @Date:   02-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 02-Sep-2017
# @License: Apache license vesion 2.0


from kivy.event import EventDispatcher
from views import Inicio

class TpvController(EventDispatcher):
    def __init__(self, **kargs):
        super(TpvController, self).__init__(**kargs)
