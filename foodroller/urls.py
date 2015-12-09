__author__ = 'stefan'

from django.conf.urls import include, url
from django.contrib import admin
from foodroller import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='catalog'),
    url(r'^categories/$', views.categories, name='catalog'),
    url(r'^roll/$', views.roll, name='catalog'),

]
