'''
Statistics to include
- Percentage of course requests fulfilled
- Number of students with empty periods (or just total number of empty periods on students' schedules)
- Number of student conflicts
- Number of teacher conflicts
- There are more but think about them later.
'''

import re

# Sections is a dictionary of section:[period, maxStudents, courseID, teacherID, room, classSize, [students]].
sections = {}

#This changes the current directory to runs
file = open('../../runs/winning_schedule.txt', 'r')
# print(file.readline()[:-1])
for x in range(file.readline()[:-1]): # 167 sections is epcific to this file. Must generalize.
    # Read every seven lines and then skip the 8th to put into sections dict.