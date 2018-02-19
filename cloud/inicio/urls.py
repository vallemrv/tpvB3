# @Author: Manuel Rodriguez <valle>
# @Date:   01-Jan-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 04-Jan-2018
# @License: Apache license vesion 2.0

from django.conf.urls import url, include
from . import views

USER = [
    url(r'^login/$', views.login, name="login_tk"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^change_password/$', views.change_password, name="change_password"),
    url(r'^reset_password/$', views.reset_password, name="password_reset"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.confirm_reset_password, name='password_reset_confirm'),
]


urlpatterns = [
    url(r'^$', views.menu_principal, name="menu_principal"),
    url(r'^not_found/$', views.not_found, name="not_found"),
    url(r'^en_construccion/$', views.en_construccion, name="en_construccion")
] + USER
