# @Author: Manuel Rodriguez <valle>
# @Date:   10-Mar-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 13-Mar-2018
# @License: Apache license vesion 2.0


from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from ventas.consumers import VentasConsumer
from django.conf.urls import url

websocket_urlpatterns = [
    url(r'^ws/$', VentasConsumer),
]
