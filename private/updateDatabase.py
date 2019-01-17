import sys
sys.path.append("/web/projects/schedule/public/scheduleServer")

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scheduleServer.settings")
import django
django.setup()

from studentInput.models import Category, Course
import re

file = open("CourseList.txt",'r',encoding = 'utf-8')
pattern = re.compile("^(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*)")

Category.objects.all().delete()

for line in file.read().splitlines():
    match = pattern.match(line)
    try:
        cat = Category.objects.get(category_text = match.group(1).strip())
    except:
        Category.objects.create(category_text = match.group(1).strip())
        cat = Category.objects.get(category_text = match.group(1).strip())
    
    cat.course_set.create(
        course_name = match.group(2).strip(),
        course_id = match.group(4).strip(),
        course_description = match.group(7).strip(),
        course_credits=match.group(5).strip(),
        course_weight = match.group(6).strip(),
    )
file.close()
    