# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   23-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Filename: floatgroup.py
# @Last modified by:   valle
# @Last modified time: 26-Feb-2018
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (ListProperty, AliasProperty, NumericProperty,
                             ReferenceListProperty, StringProperty, ObjectProperty)
from kivy.lang import Builder
import components.resources

Builder.load_string('''
<RelativeButton>:
    show: False
    size_hint: None, None
    size: 2 * root.size_button, root.size_button
    FloatButton:
        size: root.size_button, root.size_button
        bgColor: root.bgColor
        icon: root.icon
        size_hint: None, None
        pos: root.pos_button
        on_release: root.on_press

<FloatGroup>:
    size_hint: 1, 1
    content: _content
    anchor_x: 'right'
    anchor_y: 'bottom'
    AnchorLayout:
        anchor_y: 'bottom'
        anchor_x: 'center'
        size_hint: None, None
        size: 1.5*root.size_button, root._height
        canvas:
            Color:
                rgba: 1,0,0,1
            Rectangle:
                size: self.size
                pos: self.pos
        GridLayout:
            cols: 1
            size_hint: None, None
            size: root.size_button, root.size_button
            id: _content

''')

class RelativeButton(RelativeLayout):
    bgColor = StringProperty("#222222")
    icon = StringProperty(resources.FA_EDIT)
    size_button = NumericProperty('70dp')
    x_button = NumericProperty(0)
    y_button = NumericProperty(0)
    pos_button = ReferenceListProperty(x_button, y_button)
    def __init__(self, **kargs):
        super(RelativeButton, self).__init__(**kargs)

    def on_show(self, w, l):
        pass

class FloatGroup(AnchorLayout):
    content = ObjectProperty()
    buttons = ListProperty([])
    size_button = NumericProperty('70dp')

    def get__height(self):
        return len(self.buttons) * self.size_button
    _height = AliasProperty(get__height, bind=['buttons', 'size_button'])

    def __init__(self, **kargs):
        super(FloatGroup, self).__init__(**kargs)

    def on_content(self, w, l):
        for button in self.buttons:
            self.content.add_widget(button)

    def add_widget(self, widget):
        if type(widget) == RelativeButton:
            self.buttons.append(widget)
            self.content.add_widget(widget)
        else:
            super(FloatGroup, self).add_widget(widget)
