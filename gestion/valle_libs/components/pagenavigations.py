# @Author: Manuel Rodriguez <valle>
# @Date:   14-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Filename: pagenavigations.py
# @Last modified by:   valle
# @Last modified time: 15-Jul-2017
# @License: Apache license vesion 2.0

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (StringProperty, ListProperty,
                             ObjectProperty, DictProperty)
from kivy.animation import Animation
from kivy.lang import Builder

Builder.load_string('''
#:import LabelColor components.labels.LabelColor
#:import ButtonIcon components.buttons.ButtonIcon
#:import get_color kivy.utils.get_color_from_hex

<MainPage>:
    content_page: _content_page
    size_hint: 1, 1
    title_bgColor: '#ffffff'
    title: ''
    BoxLayout:
        orientation: 'vertical'
        size_hint: 1, 1
        AnchorLayout:
            id: _header
            size_hint: 1, None
            height: dp(50)
            anchor_y: 'top'
            anchor_x: 'center'
            canvas:
                Color:
                    rgb: 0,0,0
                Rectangle:
                    size: self.size
                    pos: self.pos
            LabelColor:
                size_hint: 1, .99
                text: root.title
                bgColor: root.title_bgColor
                border_size: 0
                font_size: '20dp'


        AnchorLayout:
            id: _content_page
            size_hint: 1, 1

<Page>:
    content_page: _content_page
    size_hint: 1, 1
    title_bgColor: '#ffffff'
    title: ''
    BoxLayout:
        orientation: 'vertical'
        size_hint: 1, 1
        AnchorLayout:
            id: _header
            size_hint: 1, None
            height: dp(50)
            anchor_y: 'top'
            anchor_x: 'center'
            canvas:
                Color:
                    rgb: 0,0,0
                Rectangle:
                    size: self.size
                    pos: self.pos
            LabelColor:
                size_hint: 1, .99
                text: root.title
                bgColor: root.title_bgColor
                border_size: 0
                font_size: '20dp'
            AnchorLayout:
                anchor_y: 'center'
                anchor_x: 'right'
                size_hint: .85, 1
                ButtonIcon:
                    size_hint: None, .7
                    width: dp(60)
                    text: 'back'
                    icon: res.FA_ANGLE_LEFT
                    orientation: 'horizontal'
                    font_size: '15dp'
                    border_size: 0
                    bgColor:'#ecd5c4'
                    on_release: root.parent.back_page()

        AnchorLayout:
            id: _content_page
            size_hint: 1, 1
            canvas.before:
                Color:
                    rgb: get_color(root.bgColor)
                Rectangle:
                    size: self.size
                    pos: self.pos

''')

class MainPage(RelativeLayout):
    title = StringProperty()
    title_bgColor = StringProperty("#ffffff")
    page_manager = ObjectProperty(None)

    def __init__(self, **kargs):
        super(MainPage, self).__init__(**kargs)

    def add_widget(self, widget):
        if len(self.children) < 1:
            super(MainPage, self).add_widget(widget)
        else:
            self.content_page.add_widget(widget)



class Page(RelativeLayout):
    title = StringProperty()
    title_bgColor = StringProperty("#ffffff")
    id_page = StringProperty("")
    bgColor = StringProperty("#ffffff")


    def add_widget(self, widget):
        if len(self.children) < 1:
            super(Page, self).add_widget(widget)
        else:
            self.content_page.add_widget(widget)



class PageManager(FloatLayout):
    pages = DictProperty({})
    stack_pages = ListProperty([])

    def __init__(self, **kargs):
        super(PageManager, self).__init__(**kargs)

    def add_widget(self, widget):
        try:
            widget.page_manager = self
        except:
            raise ("Error", "Widget not is MainPage or Page types")

        if type(widget) is MainPage:
            self.stack_pages.append(widget)
            super(PageManager,self).add_widget(widget)
        elif type(widget) is Page:
            widget.bind(id_page=self.on_id_pages)

    def on_id_pages(self, w, val):
        self.pages[val] = w

    def navigate(self, nav):
        w = self.pages[nav]
        w.pos = self.width+10, 0
        self.stack_pages.append(self.pages[nav])
        super(PageManager, self).add_widget(w)
        ai = Animation(x=0, duration=.1)
        ai.start(w)

    def back_page(self):
        w = self.stack_pages[-1]
        ai = Animation(x=self.width+10, duration=.1)
        ai.bind(on_complete=self.on_complete)
        ai.start(w)

    def on_complete(self, ani, w):
        w = self.stack_pages.pop()
        self.remove_widget(w)
