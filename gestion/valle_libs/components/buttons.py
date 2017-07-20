# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   09-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 18-Jul-2017
# @License: Apache license vesion 2.0

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.utils import get_color_from_hex
from kivy.properties import (ObjectProperty, StringProperty,
                             ListProperty, BooleanProperty, OptionProperty)
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.graphics.instructions import InstructionGroup
from kivy.vector import Vector
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
import resources as res
Builder.load_file(res.get_kv("buttons"))

class Decorators(AnchorLayout):
    def __init__(self, **kargs):
        super(Decorators, self).__init__(**kargs)

class ButtonBase(ButtonBehavior, Widget):
    tag = ObjectProperty(None, allownone=True)
    bgColor = StringProperty('#707070')
    font_size = StringProperty("30dp")
    container = ObjectProperty(None)
    listchild = ListProperty([])
    color = ListProperty([1, 1, 1, 1])
    shape_up = ObjectProperty(None)
    shape_down = ObjectProperty(None)

    def __init__(self, **kargs):
        super(ButtonBase, self).__init__(**kargs)

    def on_color(self, w, val):
        if "#" in val:
            val = "".join(val)
            self.color = get_color_from_hex(val)
        else:
            self.color = val

    def on_container(self, root, val):
        self.container.bind(pos=self.on_container_pos)
        for w in self.listchild:
            self.container.add_widget(w)
        self.draw_color()

    def on_listchild(self, w, val):
        if self.container != None:
            for w in self.listchild:
                self.container.add_widget(w)

    def add_widget(self, widget):
        if type(widget) is Decorators:
            super(ButtonBase, self).add_widget(widget)
        else:
            self.listchild.append(widget)


    def on_container_pos(self, root, val):
        if self.shape_up == None:
            self.shape_up = InstructionGroup(grup="shape_up")
        else:
            self.container.canvas.before.remove(self.shape_up)
            self.shape_up.clear()
        self.draw_color()

    def on_bgColor(self, root, val):
        if self.shape_up == None:
            self.shape_up = InstructionGroup(grup="shape_up")
        else:
            self.container.canvas.before.remove(self.shape_up)
            self.shape_up.clear()
        self.draw_color()

    def draw_color(self):
        if self.container and self.shape_up:
            size = self.container.size
            color = Color()
            color.rgb = get_color_from_hex(self.bgColor)
            self.shape_up.add(color)
            self.shape_up.add(Rectangle(pos=self.container.pos, size=size))
            self.container.canvas.before.add(self.shape_up)


    def collide_point(self, x, y):
        return (x > self.x and x < self.x +self.width) and (y > self.y and y < self.y +self.height)

    def on_touch_down(self, touch, *args):
        super(ButtonBase, self).on_touch_down(touch)
        if self.collide_point(touch.x, touch.y):
            size = self.container.size
            if self.shape_down == None:
                self.shape_down = InstructionGroup(group="shape_down")
            else:
                self.container.canvas.before.remove(self.shape_down)
                self.shape_down.clear()
            color = Color(0,0,0,.4)
            self.shape_down.add(color)
            self.shape_down.add(Rectangle(pos=self.container.pos, size=size))
            self.container.canvas.before.add(self.shape_down)
            Clock.schedule_once(self.remove_shape_down, .05)
            return True

    def remove_shape_down(self, dt):
        self.container.canvas.before.remove(self.shape_down)
        self.shape_down.clear()




class ButtonColor(ButtonBase):
    text = StringProperty()
    selectable = BooleanProperty(False)
    selected = BooleanProperty(False)

    def __init__(self, **kargs):
        super(ButtonColor, self).__init__(**kargs)

    def on_selected(self, w, val):
        self.label_selected.text = res.FA_CHECK if val and self.selectable else ""

    def on_press(self):
        super(ButtonColor, self).on_press()
        if self.selectable:
            self.selected = not self.selected


class ButtonImg(ButtonBase):
    src = StringProperty()
    text = StringProperty()
    label_container = ObjectProperty(None, allownone=False)

    def __init__(self, **kargs):
        super(ButtonImg, self).__init__(**kargs)

    def on_label_container(self, w, val):
        if self.text != "" and len(self.label_container.children) == 1:
            self.add_label()

    def on_text(self, w, val):
        if val != ""  and len(self.label_container.children) == 1:
            self.add_label()

    def add_label(self):
        label = Label(text=self.text, font_size=self.font_size,
                      color=self.color,size_hint= (1, .2),
                      halign= 'center', valign='middle')
        label.bind(size=label.setter("text_size"))
        self.bind(text=label.setter('text'))
        self.bind(color=label.setter('color'))
        self.bind(font_size=label.setter('font_size'))
        self.label_container.add_widget(label)

class ButtonIcon(ButtonBase):
    icon = StringProperty('')
    text = StringProperty('')
    label_container = ObjectProperty(allownone=False)
    orientation = OptionProperty("vertial", options=("vertical", "horizontal"))
    label_size_hint = ListProperty([1, .3])
    icon_size_hint = ListProperty([1, .7])
    icon_align = OptionProperty("center", options=("center","left","right"))
    icon_font_size = ObjectProperty("30dp")

    def __init__(self, **kargs):
        super(ButtonIcon, self).__init__(**kargs)

    def on_label_container(self, w, val):
        if self.text != "" and len(self.label_container.children) == 1:
            self.add_label()

    def on_text(self, w, val):
        if val != ""  and  self.label_container and len(self.label_container.children) == 1:
            self.add_label()

    def add_label(self):
        label = Label(text=self.text, font_size=self.font_size,
                      color=self.color, halign= 'center', valign='middle')
        label.bind(size=label.setter('text_size'))
        self.bind(text=label.setter('text'))
        self.bind(color=label.setter('color'))
        self.bind(font_size=label.setter('font_size'))
        self.bind(label_size_hint=label.setter('size_hint'))
        self.label_container.add_widget(label)

    def on_orientation(self, w, val):
        self.label_size_hint = (1, .3) if val == "vertical" else (.7, 1)
        self.icon_size_hint = (1, .8) if val == "vertical" else (.2, 1)
        self.icon_align = "center" if val == "vertical" else "left"

    def on_font_size(self, w, val):
        self.icon_font_size = dp(self.font_size.replace('dp','')) + dp(20)




class FloatButton(ButtonBehavior, Widget):
    bgColor = StringProperty("#108710")
    icon = StringProperty(res.FA_EDIT)
    font_size = StringProperty("30dp")
    color = ListProperty([1, 1, 1, 1])

    def __init__(self, *args, **kwargs):
        super(FloatButton, self).__init__(*args, **kwargs)
        self.shape_up = None
        self.shape_down = None

    def on_color(self, w, val):
        if "#" in val:
            val = "".join(val)
            self.color = get_color_from_hex(val)

    def on_bgColor(self, root, val):
        if self.shape_up == None:
            self.shape_up = InstructionGroup(grup="shape_up")
        else:
            self.shape.canvas.remove(self.shape_up)
            self.shape_up.clear()
        color = Color()
        color.rgb = get_color_from_hex(val)
        self.shape_up.add(color)
        self.shape_up.add(Ellipse(pos=self.shape.pos, size=self.shape.size))
        self.shape.canvas.before.add(self.shape_up)
        self.shape_up.clear()


    def collide_point(self, x, y):
        return Vector(x, y).distance(self.center) <= self.width / 2

    def on_touch_down(self, touch, *args):
        super(FloatButton, self).on_touch_down(touch)
        if self.collide_point(touch.x, touch.y):
            if self.shape_down == None:
                self.shape_down = InstructionGroup(grup="shape_down")
            else:
                self.shape.canvas.before.remove(self.shape_down)
                self.shape_down.clear()
            color = Color(0,0,0,.4)
            self.shape_down.add(color)
            self.shape_down.add(Ellipse(pos=self.shape.pos, size=self.shape.size))
            self.shape.canvas.before.add(self.shape_down)
            return True

    def on_touch_up(self, touch, *args):
        super(FloatButton, self).on_touch_up(touch)
        if self.collide_point(touch.x, touch.y):
            self.shape.canvas.before.remove(self.shape_down)
            self.shape_down.clear()
            return True
