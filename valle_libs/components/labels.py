# @Author: Manuel Rodriguez <vallemrv>
# @Date:   11-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 14-Jul-2017
# @License: Apache license vesion 2.0


from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.vector import Vector
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.graphics.instructions import InstructionGroup
from kivy.lang import Builder
from kivy.properties import (StringProperty, ObjectProperty,
                             ListProperty, OptionProperty, NumericProperty)
from kivy.clock import Clock
from math import ceil
import resources as res

Builder.load_file(res.get_kv("labels"))

class LabelDecorators(AnchorLayout):
    def __init__(self, **kargs):
        super(LabelDecorators, self).__init__(**kargs)

class LabelBase(Widget):
    bgColor = StringProperty("#4594be")
    color = StringProperty("#000000")
    text = StringProperty()
    font_size = StringProperty('30dp')
    listchild = ListProperty([])
    border_size = NumericProperty(5)


    def on_container(self, root, val):
        for w in self.listchild:
            self.container.add_widget(w)

    def on_listchild(self, w, val):
        if self.container != None:
            for w in self.listchild:
                self.container.add_widget(w)

    def add_widget(self, widget):
        if type(widget) is LabelDecorators:
            super(LabelBase, self).add_widget(widget)
        else:
            self.listchild.append(widget)

class LabelColor(LabelBase):
    def __init__(self, **kargs):
        super(LabelColor, self).__init__(**kargs)

class LabelClicableBase(ButtonBehavior, LabelBase):
    tag = ObjectProperty(None, allowNone=True)

    def __init__(self, **kargs):
       super(LabelClicableBase, self).__init__(**kargs)
       self.shape_down = None

    def collide_point(self, x, y):
        return (x > self.x and x < self.x +self.width) and (y > self.y and y < self.y +self.height)

    def on_touch_down(self, touch, *args):
        if self.collide_point(touch.x, touch.y):
            size = ceil(self.height * 0.7), ceil(self.height * 0.7)
            w, h = size
            pos = touch.x -w/ 2, touch.y - h/2
            if self.shape_down == None:
                self.shape_down = InstructionGroup(group="shape_down")
            else:
                self.container.canvas.before.remove(self.shape_down)
                self.shape_down.clear()
            color = Color(0,0,0,.4)
            self.shape_down.add(color)
            self.shape_down.add(Ellipse(pos=pos, size=size))
            self.container.canvas.before.add(self.shape_down)
            Clock.schedule_once(self.remove_shape_down, .05)
            super(LabelClicableBase, self).on_touch_down(touch)
            return True

    def remove_shape_down(self, dt):
        self.container.canvas.before.remove(self.shape_down)
        self.shape_down.clear()

class LabelClicable(LabelClicableBase):
    def __init__(self, **kargs):
        super(LabelClicable, self).__init__(**kargs)


class LabelIcon(LabelClicableBase):
    icon = StringProperty(res.FA_ANGLE_RIGHT)

    def __init__(self, **kargs):
        super(LabelIcon, self).__init__(**kargs)
