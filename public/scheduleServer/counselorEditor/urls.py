from django.urls import path

from . import views

app_name = 'counselorEditor'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),

    path('search/', views.search, name='search'),
    
    path('edit/', views.edit, name = 'edit')
]