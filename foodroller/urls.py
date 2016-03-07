from django.conf.urls.static import static
from foodroller_project import settings

__author__ = 'stefan'

from django.conf.urls import include, url, patterns
from django.contrib import admin
from foodroller import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='catalog'),
    url(r'^categories/$', views.categories, name='catalog'),
    url(r'^roll/$', views.roll, name='roll'),
    url(r'^roll-food/$', views.roll_food, name='roll_food'),
    url(r'^food/(?P<food_slug>[\w\-]+)/$', views.food_details, name='food'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search-food/$', views.set_food, name='search'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header = settings.ADMIN_SITE_HEADER
