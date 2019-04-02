from django.urls import path, include

from . import views

app_name = 'counselorEditor'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('edit/', views.edit, name = 'edit'),
    path('submit/',views.submit, name = 'submit'),
    path('upload/', views.upload, name = 'upload'),
    path('success/', views.success, name = 'success'),
    path('sections/', views.sections, name = 'sections'),
    path('input_sections/', views.input_sections, name = 'input_sections'),
    path('big_red_button/', views.big_button, name = 'big_button'),
    path('start/', views.start, name = 'start'),
    path('relation/',views.relation, name = 'relation'),
]