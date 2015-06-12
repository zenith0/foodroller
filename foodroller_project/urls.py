from django.conf.urls import include, url, patterns
from django.contrib import admin
from foodroller import views
from django.conf.urls.static import static
import settings

urlpatterns = patterns ('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^edit/(?P<dish_slug>[\w\-]+)', views.edit, name='edit'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

