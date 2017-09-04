from django.conf.urls import url

from . import views

urlpatterns = [
   url(r'^$', views.index, name="index"),
   url(r'^addseccion/$', views.add_seccion, name="add_seccion"),
   url(r'^list_seccion/$', views.list_seccion, name="list_seccion")
 ]
