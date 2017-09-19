# -*- coding: utf-8 -*-

# @Author: Manuel Rodriguez <valle>
# @Date:   10-May-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 15-Sep-2017
# @License: Apache license vesion 2.0

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (BooleanProperty, StringProperty, AliasProperty,
                             ObjectProperty, NumericProperty, ListProperty)
from kivy.lang import Builder
from kivy.metrics import dp
from components.buttons import ButtonColor, ButtonIcon
from math import ceil
import resources as res

Builder.load_string('''
#:import res components.resources
#:import ButtonIcon components.buttons.ButtonIcon
<Header>:
    font_size_title: '20dp'
    title: 'None'
    size_hint: 1, None
    height: root._height
    orientation: 'horizontal'
    Label:
        color: 0, 0, 0, 1
        text: root.title
        font_size: root.font_size_title
        size_hint: 1, 1

<Content>:
    content: _content
    content_size_hint: 1, 1
    cols: 2
    spacing: 2
    ScrollView:
        size_hint: 1, 1
        GridLayout:
            id: _content
            cols: root.cols
            spacing: root.spacing
            size_hint: root.content_size_hint


<GridButtons>:
    anchor_x: 'center'
    anchor_x: 'center'
    main: _main
    size_hint: 1, 1
    spacing: 2
    GridLayout:
        size_hint: 1, 1
        cols: 1
        spacing: 20
        id: _main


''')
class Content(AnchorLayout):
    content_size_hint = ListProperty([])
    cols = NumericProperty(1)
    spacing = NumericProperty(1)
    scrollable = BooleanProperty(False)
    def __init__(self, **kargs):
        super(Content, self).__init__(**kargs)

    def add_widget(self, w):
        if len(self.children) <= 0:
            super(Content, self).add_widget(w)
        else:
            self.content.add_widget(w)
            if self.scrollable:
                self.content.height = dp(100) * ceil(len(self.content.children) / float(self.content.cols))


    def clear_widgets(self):
        self.content.clear_widgets()

    def on_scrollable(self, w, val):
        if self.scrollable and self.content:
            self.content_size_hint = (1, None)
            self.content.height = dp(100) * ceil(len(self.content.children) / float(self.content.cols))
        else:
            self.content_size_hint = (1, 1)



class Header(BoxLayout):
    font_size_title = ObjectProperty('40dp')
    title = StringProperty("None")

    def get__height(self):
        return dp(self.font_size_title.replace('dp', '')) + dp(20)
    _height = AliasProperty(get__height, bind=['font_size_title'])

    def __init__(self, **kargs):
        super(Header, self).__init__(**kargs)

class GridButtons(AnchorLayout):
    font_size = ObjectProperty("30dp")
    font_size_title = ObjectProperty("30dp")
    fgColor = ListProperty([0,0,0,1])
    title = StringProperty("None")
    botones = ListProperty([])
    onPress = ObjectProperty(allownone=False)
    item_selected = ListProperty([])
    text_button_enter = StringProperty("sel 0")
    cols = NumericProperty(1)
    spacing = NumericProperty(2)
    main = ObjectProperty(None)
    selected = NumericProperty(0)
    scrollable = BooleanProperty(False)
    selectable = BooleanProperty(False)



    def __init__(self, **kargs):
        super(GridButtons, self).__init__(**kargs)
        self.header = Header()
        self.bind(title=self.header.setter("title"))
        self.bind(font_size_title=self.header.setter('font_size_title'))
        self.content = Content()
        self.bind(cols=self.content.setter('cols'))
        self.bind(spacing=self.content.setter('spacing'))
        self.bind(scrollable=self.content.setter('scrollable'))


    def on_main(self, w, l):
        self.main.add_widget(self.content)

    def on_title(self, w, val):
        if self.title == 'None' and len(self.main.children) == 2:
            self.main.remove_widget(self.header)
        elif self.title != 'None' and len(self.main.children) == 1 :
            self.main.clear_widgets()
            self.main.add_widget(self.header, index=0)
            self.main.add_widget(self.content)
            if self.selectable:
                self.add_button_enter()


    def on_selectable(self, w, val):
        if self.selectable and self.header and len(self.header.children) == 1:
            self.add_button_enter()
        elif not self.selectable and self.header and len(self.header.children) == 2:
            self.header.remove_widget(self.header.children[0])



    def on_item_selected(self, w, val):
        if self.header:
            if val != "" and len(self.header.children) == 1:
                self.add_button_enter()
            self.text_button_enter = "sel "+ str(len(self.item_selected))
        self.selected = len(self.item_selected)


    def add_button_enter(self):
        if self.selectable and self.header and len(self.header.children) == 1:
            btn = ButtonIcon(text=self.text_button_enter,size_hint=(.6, 1),
                        font_size='15dp', icon_scale='0dp', orientation='horizontal',icon=res.FA_ENTER)
            self.header.add_widget(btn)
            self.bind(text_button_enter=btn.setter('text'))
            btn.bind(on_release=self.on_button_enter_press)


    def on_botones(self, key, value):
        self.set_botones()

    def set_botones(self):
        self.content.clear_widgets()
        self.item_selected = []
        if len(self.botones) > 0:
            if self.cols <= 0:
                self.content.cols = self.get_columns(len(self.botones))
            else:
                self.content.cols  = self.cols
            for btn in self.botones:
                btnC = ButtonColor(tag=btn, color=self.fgColor,  selectable=self.selectable)
                if "selected" in btn:
                    btnC.selected = btn.get("selected")
                    self.item_selected.append(btnC)
                if "text" in btn:
                    btnC.text=btn.get('text')
                if "bgColor" in btn:
                    btnC.bgColor = btn.get('bgColor')
                if "icon" in btn:
                    btnC.font_name = res.FONT_AWESOME
                    btnC.text = btn.get("icon")
                btnC.font_size = self.font_size
                btnC.bind(on_press=self.on_press)
                self.bind(selectable=btnC.setter('selectable'))
                self.content.add_widget(btnC)

    def get_columns(self, num):
        if num <= 5:
            return 1
        elif num > 5 and num < 10:
            return 3
        elif num >= 10:
            return 4

    def on_exit(self):
        self.onPress(self.item_selected)

    def on_button_enter_press(self, btn):
        if self.onPress:
            self.onPress(self.item_selected)

    def on_press(self, btn):
        if self.selectable:
            if not btn.selected:
                self.item_selected.append(btn)
            else:
                self.item_selected.remove(btn)
        elif self.onPress:
            self.onPress([btn])
