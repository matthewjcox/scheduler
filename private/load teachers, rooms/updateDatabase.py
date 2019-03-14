import sys
sys.path.append("/web/projects/schedule/public/scheduleServer")

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scheduleServer.settings")
import django
django.setup()

from studentInput.models import Teacher,Room
import re

file = open("TeacherList.txt",'r',encoding = 'utf-8')
pattern = re.compile("^(.*?), (.*?), (.*)")

Teacher.objects.all().delete()

for line in file.read().splitlines():
    match = pattern.match(line)
    Teacher.objects.create(
        teacher_first_name = match.group(1).strip(),
        teacher_last_name = match.group(2).strip(),
        teacher_id = match.group(3).strip(),
    )
        
file.close()




file = open("RoomList.txt",'r',encoding = 'utf-8')

Room.objects.all().delete()

for line in file.read().splitlines():
    Room.objects.create(rmNum = line.strip())

file.close()








