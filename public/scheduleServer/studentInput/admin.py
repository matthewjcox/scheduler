from django.contrib import admin

# Register your models here.

from .models import Category, Course, Student

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Student)