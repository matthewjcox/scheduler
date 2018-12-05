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

# First command line argument: file with run data to interpret
toInterpret = sys.argv[1]  # Currently, ../../runs/perfect_schedule.txt
# Second command line argument: file with course information used in that run
coursesText = sys.argv[2]  # Currently, ../../runs/constraint_files/courses.txt
# Third command line argument: file with teacher information used in that run
teachersText = sys.argv[3]  # Currently, ../../runs/constraint_files/teamed_3_teachers.txt

# Opens the file with run information to analyze
file = open(toInterpret, 'r')

# Sections is a dictionary of sectionID:[secionID, period, maxStudents, courseID, [teacherIDs], room, classSize, [students], [teamed courses]].
sections = {}

# Initiates a for-loop that runs once for every section in the schedule
for x in range(int(file.readline()[:-1])):
    # Reads the data with the sectionID and stores it in "section" as a string.
    line = file.readline()[2:-1]
    section = re.search('[0-9]+', line).group(0)
    # Adds sectionID to the list associated with sectionID. Redundant, but useful for for-loops that loop over items in sections.values().
    # Also adds period to sections[section] as an int.
    sections[section] = [section, int(file.readline()[10])]
    # Adds max students to sections[section] as an int.
    sections[section].append(int(file.readline()[21:-1]))
    # Adds courseID to sections[section] as a string.
    sections[section].append(re.search(r'[0-9A-Z]+', file.readline()[13:-1]).group(0))
    # Adds a list of teachers to section[sections] using teacher's IDs (amreid, for instance).
    sections[section].append([re.search(r'\(.+\)', curLine).group(0)[1:-1] for curLine in file.readline()[14:-1].split(", ")])
    # Adds room to section[sections] as a string.
    sections[section].append(file.readline()[16:-1])
    # Reads line with student data. Stored so as to be able to access multiple times.
    nextLine = file.readline()
    # Adds class size to sections[section] as an int.
    sections[section].append(int(re.search(r'\([0-9]+\)', nextLine[13:-1]).group(0)[1:-1]))
    # Adds an empty list to section[sections] if the section has no students.
    if sections[section][6] == 0:
        sections[section].append([])
    # Adds a list of students, represented by student numbers held as strings, to sections[section] if class size > 0.
    else:
        sections[section].append([re.search(r'\([0-9]+\)', curLine).group(0)[1:-1] for curLine in re.search(': .*', nextLine).group(0)[2:].split(", ")])
    # Reads the next line to check if it has teaming data.
    nextLine = file.readline()
    # If the next line has teaming data, adds teaming data to sections[section] as list of strings of section IDs/
    if re.search('Teamed with:', nextLine):
        sections[section].append([re.search('[0-9]+', curLine).group(0) for curLine in nextLine[15:-1].split(", ")])
        file.readline()
    # If next line does not have teaming data, adds an empty list to sections[section] to represent no teaming.
    else:
        sections[section].append([])
    # Prints sections[section] for debugging.
    #print(sections[section])

# students is a dictionary of studentID:[studentID, [course requests], [alternates], [sections]], with course and section info in IDs.
students = {}

# Initiates a for-loop that runs for each student in the case.
for x in range(int(file.readline()[:-1])):
    # Finds the student ID of the current student as a string.
    curStud = re.search(r'\(.*\)', file.readline()).group(0)[1:-1]
    # Adds the student number as a key in students and initiats a list as the associated value with the first element as the student ID.
    students[curStud] = [curStud, [], [], []]
    nextLine = file.readline()
    while not re.search('Alternates:', nextLine):
        students[curStud][1].append(re.search(r'\w*(?= )', nextLine).group(0))
        nextLine = file.readline()
    nextLine = file.readline()
    while not re.search('None', nextLine) and not re.search('Schedule:', nextLine):
        students[curStud][2].append(re.search(r'\w*(?= )', nextLine).group(0))
        nextLine = file.readline()
    if re.search('None', nextLine):
        file.readline()
    nextLine = file.readline()
    while not nextLine == "\n":
        students[curStud][3].append(re.search(r'\w*(?=:)', nextLine[9:]).group(0))
        nextLine = file.readline()
    print(students[curStud])