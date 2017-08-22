# @Author: Manuel Rodriguez <valle>
# @Date:   20-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Filename: config.py
# @Last modified by:   valle
# @Last modified time: 11-Aug-2017
# @License: Apache license vesion 2.0

from kivy.event import EventDispatcher
from kivy.properties import StringProperty

class Config(EventDispatcher):
    #servidor = StringProperty("https://themagicapi.valleapp.com")
    servidor = StringProperty("http://localhost:8000")
    token = StringProperty("4nw-5633f58ea70749868236")
    user = StringProperty("1")
    db = StringProperty('btressl')
    def __init__(self, **kargs):
        super(Config, self).__init__(**kargs)
