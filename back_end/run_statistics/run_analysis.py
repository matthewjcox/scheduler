'''
Statistics to include
- Percentage of course requests fulfilled
- Number of students with empty periods (or just total number of empty periods on students' schedules)
- Number of student conflicts
- Number of teacher conflicts
- There are more but think about them later.
'''

import re
import sys

toInterpret = sys.argv[1]
coursesText = sys.argv[2]
teachersText = sys.argv[3]

# Sections is a dictionary of section:[period, maxStudents, courseID, [teacherIDs], room, classSize, [students], [teamed courses]].
sections = {}

#This changes the current directory to runs
file = open(toInterpret, 'r')
# print(file.readline()[:-1])
for x in range(int(file.readline()[:-1])): # 167 sections is epcific to this file. Must generalize.
    # Read every seven lines and then skip the 8th to put into sections dict.
    line = file.readline()[2:-1]
    section = re.search('[0-9]+', line).group(0)
    sections[section] = [section, int(file.readline()[10])]
    sections[section].append(int(file.readline()[21:-1]))
    sections[section].append(re.search(r'[0-9A-Z]+', file.readline()[13:-1]).group(0))
    sections[section].append([re.search(r'\(.+\)', curLine).group(0)[1:-1] for curLine in file.readline()[14:-1].split(", ")])
    sections[section].append(file.readline()[16:-1])
    # Reads line with student data. Stored so as to be able to access multiple times.
    nextLine = file.readline()
    sections[section].append(int(re.search(r'\([0-9]+\)', nextLine[13:-1]).group(0)[1:-1]))
    if sections[section][6] == 0:
        sections[section].append([])
    else:
        sections[section].append([re.search(r'\([0-9]+\)', curLine).group(0)[1:-1] for curLine in re.search(': .*', nextLine).group(0)[2:].split(", ")])
    nextLine = file.readline()
    if re.search('Teamed with:', nextLine):
        sections[section].append([re.search('[0-9]+', curLine).group(0) for curLine in nextLine[15:-1].split(", ")])
        file.readline()
    else:
        sections[section].append([])
    print(sections[section])