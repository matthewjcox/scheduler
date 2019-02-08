'''
Rules to follow:
 - Teachers with only periods in {1, 2, 3, 4} are part-time on blue days, so all classes will have
   allowed periods of 1, 2, 3, 4. Same for {5, 6 ,7} and red days.
 - Semester courses that end up in the same period will be seen as constrained to be in the same period
 - Semester courses that are sem 1 will be seen as constrained to be in sem 1. Same for sem 2.
 - Homerooms will be ignored.
 - Room will be included as a constraint
 - Arabic key MUST be used to create list
    - Arabics are teamed

 - Teaming:
    - team_1: Sections teamed to have same students and different periods
    - team_2: Sections teamed to have different students and same period
        - Orchestra
        - team_period
    - team_3: Sections teamed to have the same students and same period, provided that students have requested class
        - Arabics
        - team_period_students
'''

from openpyxl import load_workbook
import re

secList = load_workbook(filename='../../runs/constraint_files/SecList 8-14@1300.xlsx')
secSheet = secList['D1BC6ACA-A78F-4688-9C6D-42D84ED']

# Sections is a dict of sections coded as follows: {secID: [(0) courseID, (1) term, (2) course title, (3) teacher, (4) room, (5) max, (6) [team1], (7) [team2], (8) [team3], (9) [allowedPeriods]}
sections = {}
# {teacher: [[(0) secID, (1) period, (2) term, (3) courseID, (4) courseTitle, (5) room, (6) cap]]}
# NOTE: term notated as follows: 0 = year, 1 = semester 1, 2 = semester 2
teacherToSects = {}

teamings = load_workbook(filename='../../runs/constraint_files/Arabic and LS to Semesters.xlsx')
arabics = teamings['Sheet1']
learningSems = teamings['Sheet2']

teamedToSems = {}
semsToTeam = {}

# Read in data from teaming workbook
for r in range(2, 28):
    curTeam = arabics.cell(row=r, column=1).value
    curSem1 = arabics.cell(row=r, column=10).value
    curSem2 = arabics.cell(row=r, column=21).value
    teamedToSems[curTeam] = {curSem1, curSem2}
    semsToTeam[curSem1] = curTeam
    semsToTeam[curSem2] = curTeam
for r in range(2, 26):
    curTeam = learningSems.cell(row=r, column=1).value
    curSem1 = learningSems.cell(row=r, column=10).value
    curSem2 = learningSems.cell(row=r, column=21).value
    teamedToSems[curTeam] = [curSem1, curSem2]
    semsToTeam[curSem1] = curTeam
    semsToTeam[curSem2] = curTeam

for r in range(2, 859):
    if secSheet.cell(row=r, column=2).value == 8:
        continue
    if secSheet.cell(row=r, column=6).value:
        teacher = secSheet.cell(row=r, column=6).value
    elif secSheet.cell(row=r, column=5).value == "See Counselor":
        teacher = "Counselor"
    elif re.search(r'Health & PE', secSheet.cell(row=r, column=5).value):
        teacher = "Gym"
    else:
        teacher = "None"
    # Will post-process on "Gym." "None" and "Counselor" mean the teacher field should be removed, but counselor designation may be helpful later.
    if not teacher in teacherToSects.keys():
        teacherToSects[teacher] = []
    teacherToSects[teacher].append([])
    teacherToSects[teacher][-1].append(secSheet.cell(row=r, column=1).value)
    teacherToSects[teacher][-1].append(secSheet.cell(row=r, column = 2).value)
    term = secSheet.cell(row=r, column=3).value
    if term == "YR":
        term = 0
    elif term == "S1":
        term = 1
    elif term == "S2":
        term = 2
    teacherToSects[teacher][-1].append(term)
    teacherToSects[teacher][-1].append(secSheet.cell(row=r, column =4).value.__str__())
    teacherToSects[teacher][-1].append(secSheet.cell(row=r, column=5).value)
    teacherToSects[teacher][-1].append(secSheet.cell(row=r, column=7).value)
    teacherToSects[teacher][-1].append(secSheet.cell(row=r, column=9).value)

for teacher in teacherToSects.keys():
    if teacher == "Gym":
        # Handle gym classes here
    if teacher == "Counselor":
        # Handle see counselors here
    if teachr == "None":
        # Handle classes lacking teachers here
    perDist = {l:[] for l in range(1,8)}
    for x in range(len(teacherToSects[teacher])):
        perDist[teacherToSects[x][1]].append(x)
    #Just testing
