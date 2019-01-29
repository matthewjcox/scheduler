from django.urls import path

from . import views

app_name = 'projectIndex'
urlpatterns = [
    path('', views.index, name='index'),
    path('studentInput/',views.redirectS, name='student'),
    path('counselorEditor/', views.redirectC, name='counselor'),
    path('teacherView/',views.redirectT, name='teacher'),
]