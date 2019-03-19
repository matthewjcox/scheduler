import sys
sys.path.append("/web/projects/schedule/public/scheduleServer")

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scheduleServer.settings")
import django
django.setup()


from studentInput.models import Category, Course, Section

file = open("Sections.txt",'w',encoding = 'utf-8')
counter = 0;
for course in Course.objects.all():
    for section in course.section_set.all():
        counter+= 1
        file.write(counter)
        file.write("\nteacher: ")
        file.write(section.teachers.all())
        file.write("\ncourseID: ")
        file.write(course.coures_id)
        file.write("\nroom: ")
        file.write(section.room)
        file.write("\nsemester: ")
        file.write("0")
        file.write("\nmaxstudents: ")
        file.write(section.students_num_max)
file.close()