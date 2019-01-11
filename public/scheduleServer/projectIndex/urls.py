from django.urls import path

from . import views

app_name = 'projectIndex'
urlpatterns = [
    path('', views.index, name='index'),
    path('oauthProcessing/', views.oauthProcessing, name = 'oauthProcessing')
]