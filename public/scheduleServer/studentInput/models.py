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
    course_id = models.CharField(max_length = 12)
    course_description = models.CharField(max_length=10000)
    course_credits = models.FloatField(default = 0.5)
    course_weight = models.FloatField(default = 0.5)
#    course_prerequisites = set()

class Student(models.Model):
    def __str__(self):
        return self.student_id
    student_id = models.CharField(max_length = 50)
    student_course_request = models.ManyToManyField(Course)
    student_first_name = models.CharField(max_length = 50)
    student_last_name = models.CharField(max_length = 50)
    
class Teacher(models.Model):
    def __str__(self):
        return self.teacher_id
    teacher_id = models.CharField(max_length = 50)
    teacher_first_name = models.CharField(max_length = 50)
    teacher_last_name = models.CharField(max_length = 50)
    
class Room(models.Model):
    rmNum = models.CharField(max_length = 15)

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    teachers = models.ManyToManyField(Teacher)
    room = models.ForeignKey(Room, on_delete = models.SET_NULL, null = True)
    students_num_max = models.IntegerField()
    period = models.IntegerField()