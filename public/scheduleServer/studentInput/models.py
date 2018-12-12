from django.db import models

# Create your models here.

    
class Category(models.Model):
    def __str__(self):
        return self.category_text
    category_text = models.CharField(max_length = 50)
    

class Course(models.Model):
    def __str__(self):
        return self.course_name
    category = models.ForeignKey(Category, on_delete = models.CASCADE) #cascade is filler, 
    #category = models.ForeignKey(Category, on_delete = models.SET_DEFAULT) <- need to figure this out
    course_name = models.CharField(max_length = 100)
    course_id = models.CharField(max_length = 7)
    course_description = models.CharField(max_length=1000)
    course_credits = models.FloatField(default = 0.5)
    course_weight = models.FloatField(default = 0.5)
#    course_prerequisites = set()

class Student(models.Model):
    def __str__(self):
        return self.student_id
    student_id = models.CharField(max_length = 50)
    student_course_request = models.ManyToManyField(Course)