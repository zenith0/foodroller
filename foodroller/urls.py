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
    url(r'^roll/$', views.roll, name='catalog'),
    url(r'^food/(?P<food_slug>[\w\-]+)/$', views.food, name='food'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header = settings.ADMIN_SITE_HEADER
