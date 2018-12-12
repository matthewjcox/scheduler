'''
NOTE: Code assumes files are stored in folders with a file called read_params.txt, and that all files listed in
read_params.txt are in that folder as well.

Statistics to include
- Percentage of course requests fulfilled
- Number of students with empty periods (or just total number of empty periods on students' schedules)
- Number of student conflicts
- Number of teacher conflicts
- There are more but think about them later.

Figure out what Young can transfer to us.
Add mean empty seats and standard deviations per course to statistics.
'''

import re
import sys
import statistics
import tabulate

# First command line argument: file with run data to interpret
toInterpret = sys.argv[1]  # Currently, ../../runs/perfect_schedule.txt

directory = re.search('/.*', toInterpret[::-1]).group(0)[::-1][:-1]

runParamsFile = open(directory + "/run_params.txt")
# runParams is an array of the run paramters (text files used in run). [(0) periods in a day, (1) classrooms.txt, (2) courses.txt, (3) teachers.txt, (4) students.txt, (5) sections.txt]
runParams = [line.strip() for line in runParamsFile.readlines()]
print(runParams)

# Creates dictionary of course IDs to relevant info about courses from the courses.txt file
courseFile = open(directory +"/" + runParams[2])
# FIX THIS COMMAND SO IT BUILDS THE CORRECT DICTIONARY!!!!
print([line.split("| ") for line in courseFile.readlines()])
courses = {course[2]:course[:2] + [course[3]] for course in [line.split("| ") for line in courseFile.readlines()]}
print(courses)

# Opens the file with run information to analyze
file = open(toInterpret, 'r')

# Sections is a dictionary of sectionID:[(0) secionID, (1) period, (2) maxStudents, (3) courseID, (4) [teacherIDs], (5) room, (6) classSize, (7) [students], (8) [teamed courses]].
sections = {}

numSections = int(file.readline()[:-1])
# Initiates a for-loop that runs once for every section in the schedule
for x in range(numSections):
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
    # print(sections[section])

# students is a dictionary of studentID:[(0) studentID, (1) [course requests], (2) [alternates], (3) [sections], (4) [courses received]], with course and section info in IDs.
studentScheds = {}

numStuds = int(file.readline()[:-1])
# Initiates a for-loop that runs for each student in the case.
for x in range(numStuds):
    # Finds the student ID of the current student as a string.
    curStud = re.search(r'\(.*\)', file.readline()).group(0)[1:-1]
    # Adds the student number as a key in studentScheds and initiats a list as the associated value with the first element as the student ID.
    studentScheds[curStud] = [curStud, [], [], []]
    nextLine = file.readline()
    while not re.search('Alternates:', nextLine):
        studentScheds[curStud][1].append(re.search(r'\w*(?= )', nextLine).group(0))
        nextLine = file.readline()
    nextLine = file.readline()
    while not re.search('None', nextLine) and not re.search('Schedule:', nextLine):
        studentScheds[curStud][2].append(re.search(r'\w*(?= )', nextLine).group(0))
        nextLine = file.readline()
    if re.search('None', nextLine):
        file.readline()
    nextLine = file.readline()
    while not nextLine == "\n":
        studentScheds[curStud][3].append(re.search(r'\w*(?=:)', nextLine[9:]).group(0))
        nextLine = file.readline()
    #print(studentScheds[curStud])

for student in studentScheds.values():
    student.append([])
    for section in student[3]:
        student[4].append(sections[section][3])
    #print(student)

# Creates a statistic file named for the file plus _stats
statFile = open(toInterpret[:-4] + "_stats.txt", "w")

theoreticalEmptySeats = (sum([sect[2] for sect in sections.values()]) - numStuds*7)
statFile.write("Minimum Empty Seats: " + theoreticalEmptySeats.__str__() + "\n")
emptySeats = sum([sect[2]-sect[6] for sect in sections.values()])
statFile.write("Empty seats: " + emptySeats.__str__() + "\n")
statFile.write("Number of empty spots in student schedules: " + (emptySeats-theoreticalEmptySeats).__str__() + "\n")

# Calculate percent course requests fulfilled
totalRequests = 0
fulfilledRequests = 0
unrecievedCourses = {}
for student in studentScheds.values():
    unfulfilledSet = {*student[1]}.difference({*student[4]})
    totalRequests += len(student[1])
    fulfilledRequests += len(student[1]) - len(unfulfilledSet)
    for sect in unfulfilledSet:
        if sect in unfulfilledSet:
            unrecievedCourses[sect] = 0
        unrecievedCourses[sect] += 1
percentFulfilled = (fulfilledRequests/totalRequests*100).__str__() + "%"
statFile.write("Percentage of Course Requests Fulfilled: " + percentFulfilled + "\n")

# Calculate number of student conflicts (number of periods during which one student has two sections)
studentConflicts = 0
studentsWithConflicts = []
for student in studentScheds.values():
    periods = {}
    for sect in student[3]:
        per = sections[sect][1]
        if not per in periods.keys():
            periods[per] = 0
        periods[per] += 1
    newConflicts = sum([0 if period <= 1 else 1 for period in periods.values()])
    studentConflicts += newConflicts
    if newConflicts > 0:
        studentsWithConflicts.append(student[0])
statFile.write("Number of student conflicts: " + studentConflicts.__str__() + "\n")
statFile.write("Students with conflicts: ")
if studentsWithConflicts:
    statFile.write( ", ".join(studentsWithConflicts) + "\n")
else:
    statFile.write("None\n")

# Calculate number of teacher conflicts (number of periods during which one teacher has two sections)
teacherCons = {}
for sect in sections.values():
    for teacher in sect[4]:
        if not teacher in teacherCons.keys():
            teacherCons[teacher] = []
        teacherCons[teacher].append(sect[1])
teachersWithCons = []
teacherConflicts = 0
for teacher in teacherCons.keys():
    periods = {}
    for period in teacherCons[teacher]:
        if not period in periods.keys():
            periods[period] = 0
        periods[period] += 1
    newConflicts = sum([0 if period <= 1 else 1 for period in periods.values()])
    teacherConflicts += newConflicts
    if newConflicts > 0:
        teachersWithCons.append(teacher)
statFile.write("Number of teacher conflicts: " + teacherConflicts.__str__() + "\n")
statFile.write("Teachers with conflicts: ")
if teachersWithCons:
    statFile.write(", ".join(teachersWithCons) + "\n")
else:
    statFile.write("None\n")

# Calculate the number of sections with class sizes exceeding maxStudents

# Calculate the number of seats available each period

# Calculate the mean empty seats and standard deviation for each course
courseToEmpty = {}
for sect in sections.values():
    curCourse = sect[3]
    if not curCourse in courseToEmpty.keys():
        courseToEmpty[curCourse] = []
    courseToEmpty[curCourse].append(sect[2]-sect[6])
table = {"Course":[*courseToEmpty.keys()], "Mean Empty Spaces":[sum(courseToEmpty[course])/len(courseToEmpty[course]) for course in courseToEmpty.keys()], "Standard Deviation":[statistics.stdev(courseToEmpty[course])if len(courseToEmpty[course]) > 1 else "Undefined" for course in courseToEmpty.keys()]}
statFile.write("\n")
statFile.write(tabulate.tabulate(table, headers="keys", tablefmt="grid"))
'''statFile.write('\nCourse\t|\tMean Empty Spaces\t|\tStandard Deviation\n-----------------------------------------------------------\n')
for course in courseToEmpty.keys():
    if len(courseToEmpty[course]) > 1:
        statFile.write('{}\t|\t{}\t|\t{}\n'.format(course, sum(courseToEmpty[course])/len(courseToEmpty[course]), statistics.stdev(courseToEmpty[course])))
    else:
        statFile.write('{}\t|\t{}\t|\t{}\n'.format(course, sum(courseToEmpty[course])/len(courseToEmpty[course]), "Undefined"))'''