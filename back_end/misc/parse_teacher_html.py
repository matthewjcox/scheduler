import re

'''
file = open("runs/constraint_files/teachers_html.txt", "r")
newFile = open("runs/constraint_files/teachers_html_minus_<>.txt", "w")
temp = re.sub(r'<.*?>', "", file.read())
newFile.write(re.sub(r'&amp;', "&", temp))
'''

'''
file = open("runs/constraint_files/teachers_html_minus_<>.txt", "r")
newFile = open("runs/constraint_files/full_teachers_prelim.txt", "w")
for line in file.read().splitlines():
    if re.match(r' {88}[^ ]', line):
        newFile.write(re.sub(r' {88}', "", line) + "\n")
'''

#'''
file = open("runs/constraint_files/full_teachers_prelim.txt", "r")
newFile = open("runs/constraint_files/full_teachers.txt", "w")

x = 0
teachers = []
for line in file.read().splitlines():
    x += 1
    if x == 1:
        teachers.append(line.strip().split(", ")[::-1])
    if x == 3:
        teachers[-1].append(line.strip()[:-9])
        x=0
        newFile.write(", ".join(teachers[-1]) + "\n")

#'''