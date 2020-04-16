#from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'lists'
urlpatterns = [
    #Домашняя страница
    #path('', views.home_page, name='home'),
    #path('/lists/one_in_the_world_list/', views.view_list, name = 'view_list'),
    url(r'^new$', views.new_list, name = 'new_list'),
    url(r'^(\d+)/$', views.view_list,
        name='view_list'),
    url(r'^(\d+)/add_item$', views.add_item, name = 'add_item'),
    ]
