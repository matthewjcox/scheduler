import re

'''
file = open("runs/constraint_files/teachers_html.txt", "r")
newFile = open("runs/constraint_files/teachers_html_minus_<>.txt", "w")
temp = re.sub(r'<.*?>', "", file.read())
newFile.write(re.sub(r'&amp;', "&", temp))
'''

#'''
file = open("runs/constraint_files/teachers_html_minus_<>.txt", "r")
newFile = open("runs/constraint_files/full_teachers.txt", "w")
for line in file.read().splitlines():
    if re.match(r' {88}[^ ]', line):
        newFile.write(re.sub(r' {88}', "", line) + "\n")
#'''