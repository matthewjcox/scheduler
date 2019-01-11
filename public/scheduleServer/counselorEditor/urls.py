from django.urls import path, include

from . import views

app_name = 'counselorEditor'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),

    path('search/', views.search, name='search'),
    
    path('edit/', views.edit, name = 'edit'),
    
    path('upload/', views.upload, name = 'upload'),
    
    path('success/', views.success, name = 'success'),
    
    path('big_red_button/', views.big_red_button, name = 'big_red_button')
]