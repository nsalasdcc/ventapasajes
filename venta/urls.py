from django.conf.urls import patterns, url

from venta import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^recorrido/(?P<id_recorrido>\d+)/$', views.detalle, name='detalle'),
    url(r'^buscar/$', views.buscar, name='buscar'),
    url(r'^confirmar/(?P<id_recorrido>\d+)/(?P<sid_asiento>[A-Fa-f0-9]+)/$', views.confirmar, name='confirmar'),
    url(r'^vender/(?P<sid_asiento>[A-Fa-f0-9]+)/$', views.vender, name='vender'),
    url(r'^cambiar/$', views.cambiar, name='cambiar'),
    url(r'^cambiacion/$', views.cambiacion, name='cambiacion'),
    url(r'^cambiacion/(?P<sid_asiento>[A-Fa-f0-9]+)/$', views.do_cambiar, name='do_cambiar'),
    url(r'^devolver/$', views.devolver, name='devolver'),
    url(r'^devolucion/$', views.devolucion, name='devolucion'),
    url(r'^devolucion/(?P<sid_asiento>[A-Fa-f0-9]+)/$', views.do_devolver, name='do_devolver'),
)