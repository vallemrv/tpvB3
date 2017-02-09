from kivy.uix.button import Button
from kivy.lang import Builder

Builder.load_string('''
<BotonImg>:
    size_hint: None, 1
    width: self.height
    src: './img/plus.ico'
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        size: root.size
        pos: root.pos
        Image:
            source: root.src
            allow_stretch: True
            center: self.parent.center
            size: root.width * .85, root.height * .85
                    ''')


class BotonImg(Button):
    pass
