import sys
sys.path.append("/web/projects/schedule/public/scheduleServer")

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scheduleServer.settings")
import django
django.setup()


from studentInput.models import Category, Course, Student

file = open("studentRequests.txt",'w',encoding = 'utf-8')

for student in Student.objects.all():
    file.write(student.student_id)
    file.write(', ')
    file.write(student.student_first_name)
    file.write(', ')
    file.write(student.student_last_name)
    file.write(', ')
    file.write(str(len(student.student_course_request.all())))
    file.write('\n')
    for course in student.student_course_request.all():
        file.write(course.course_id)
        file.write('\n')
    file.write("\n")
file.close()