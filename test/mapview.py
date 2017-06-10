from kivy.garden.mapview import MapView
from kivy.app import App

class MapViewApp(App):
    def build(self):
        mapview = MapView(zoom=50, lat=50.6394, lon=3.057)
        return mapview

MapViewApp().run()
