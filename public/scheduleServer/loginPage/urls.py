from django.urls import path,re_path

from . import views

app_name = 'loginPage'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^redirect/$', views.redirect, name = 'redirect')
]