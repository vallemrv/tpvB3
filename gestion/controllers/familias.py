# @Author: Manuel Rodriguez <valle>
# @Date:   16-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Filename: productos.py
# @Last modified by:   valle
# @Last modified time: 16-Jul-2017
# @License: Apache license vesion 2.0


from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder

Builder.load_string('''
#:import FloatButton  components.buttons.FloatButton
<Familias>:
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'

    AnchorLayout:
        anchor_x: 'right'
        anchor_y: 'bottom'
        AnchorLayout:
            anchor_y: 'center'
            anchor_x: 'center'
            size_hint:None, None
            size: dp(100),dp(100)
            FloatButton:
                bgColor: '#8ec0fb'
                icon: res.FA_PLUS
                size_hint: None, None
                size: dp(70), dp(70)
                    ''')


class Familias(AnchorLayout):
    def __init__(self, **kargs):
        super(Familias, self).__init__(**kargs)
