from django.urls import path

from . import views

app_name = 'studentInput'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),

    path('course_selection/', views.course_selection, name='course_selection'),
    
    path('course_selection/submit/', views.submit, name='submit'),
]