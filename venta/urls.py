from django.conf.urls import patterns, url

from venta import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)