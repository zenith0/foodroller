from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from foodroller.views import RollView, Categories, FoodDetails, SearchFood, RollFood, SummaryView, \
    PlanDetails, Plans, CategoryDetails, ManageCategories, CreateCategory, DeleteCategory, UpdateCategory, ManageFood, \
    DeleteFood, UpdateFood, index
from foodroller_project import settings

__author__ = 'stefan'

from django.conf.urls import include, url, patterns
from django.contrib import admin
from foodroller import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^food/$', login_required(Categories.as_view(), login_url="/"), name='catalog'),
    url(r'^category/add/$', login_required(CreateCategory.as_view(), login_url="/"), name='create_category'),
    url(r'^category/delete/(?P<slug>[\w\-]+)/$', login_required(DeleteCategory.as_view(), login_url="/"), name='delete_category'),
    url(r'^category/update/(?P<slug>[\w\-]+)/$', login_required(UpdateCategory.as_view(), login_url="/"), name='update_category'),
    url(r'^category/(?P<slug>[\w\-]+)/$', login_required(CategoryDetails.as_view(), login_url="/"), name='categories'),
    url(r'^roll/$', login_required(RollView.as_view(), login_url="/"), name='roll'),
    url(r'^roll-food/$', login_required(RollFood.as_view(), login_url="/"), name='roll_food'),
    url(r'^food/(?P<slug>[\w\-]+)/$', login_required(FoodDetails.as_view(), login_url="/"), name='food'),
    url(r'^search/$', login_required(SearchFood.as_view(), login_url="/"), name='search'),
    url(r'^summary/$', login_required(SummaryView.as_view(), login_url="/"), name='summary'),
    url(r'^plans/$', login_required(Plans.as_view(), login_url="/"), name='plans'),
    url(r'^plans/(?P<slug>[\w\-]+)/$', login_required(PlanDetails.as_view(), login_url="/"), name='plans'),
    url(r'^deleteplan/(?P<slug>[\w\-]+)/$', login_required(views.delete_details, login_url="/"), name='deleteplan'),
    url(r'^manage/$', login_required(ManageCategories.as_view(), login_url="/"), name='manage'),
    url(r'^manage/category/(?P<slug>[\w\-]+)/$', login_required(ManageFood.as_view(), login_url="/"), name='manage_food'),
    url(r'^manage/category/(?P<cat_slug>[\w\-]+)/food/delete/(?P<slug>[\w\-]+)/$', login_required(DeleteFood.as_view(), login_url="/"), name='delete_food'),
    url(r'^manage/category/(?P<cat_slug>[\w\-]+)/food/update/(?P<slug>[\w\-]+)/$', login_required(UpdateFood.as_view(), login_url="/"), name='delete_food'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header = settings.ADMIN_SITE_HEADER
