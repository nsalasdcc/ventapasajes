from django.conf.urls import patterns, url

from venta import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^recorrido/(?P<id_recorrido>\d+)/$', views.detalle, name='detalle'),
)