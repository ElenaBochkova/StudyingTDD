from django.urls import path

from . import views

app_name = 'lists'
urlpatterns = [
    #Домашняя страница
    path('', views.home_page, name='home'),
    ]
