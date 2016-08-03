from django.conf.urls.static import static
from foodroller.views import RollView, FoodPreview, Categories, FoodDetails, SearchFood, RollFood, SummaryView, \
    PlanDetails, Plans, CategoryDetails, ManageCategories
from foodroller_project import settings

__author__ = 'stefan'

from django.conf.urls import include, url, patterns
from django.contrib import admin
from foodroller import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', FoodPreview.as_view(), name='index'),
    url(r'^food/$', Categories.as_view(), name='catalog'),
    url(r'^category/(?P<slug>[\w\-]+)/$', CategoryDetails.as_view(), name='categories'),
    url(r'^roll/$', RollView.as_view(), name='roll'),
    url(r'^roll-food/$', RollFood.as_view(), name='roll_food'),
    url(r'^food/(?P<slug>[\w\-]+)/$', FoodDetails.as_view(), name='food'),
    url(r'^search/$', SearchFood.as_view(), name='search'),
    url(r'^summary/$', SummaryView.as_view(), name='summary'),
    url(r'^plans/$', Plans.as_view(), name='plans'),
    url(r'^plans/(?P<slug>[\w\-]+)/$', PlanDetails.as_view(), name='plans'),
    url(r'^deleteplan/(?P<slug>[\w\-]+)/$', views.delete_details, name='deleteplan'),
    url(r'^manage/$', ManageCategories.as_view(), name='manage'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header = settings.ADMIN_SITE_HEADER
