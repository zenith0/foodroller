from django.conf.urls import include, url, patterns
from django.contrib import admin
from dishes import views
from django.conf.urls.static import static
import settings

urlpatterns = patterns ('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^add', views.add, name='add'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

