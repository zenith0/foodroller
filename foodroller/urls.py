from django.conf.urls import include, url
from django.contrib import admin
from dishes import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'foodroller.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^add/', views.add, name='add'),
]
