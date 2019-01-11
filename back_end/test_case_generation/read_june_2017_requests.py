from openpyxl import load_workbook

wb = load_workbook(filename='../../runs/constraint_files/6-1-17@1430.xlsx')
ws = wb['Sheet1']

file = open("../../runs/constraint_files/full_school_2017_students.txt", "w")

'''curStud = ws.cell(row=2,column=1).value
# ADJUST THE AUTOMATIC 7 COURSES TO BE INTELLIGENT!
file.write(curStud.__str__() + ", Student, " + curStud.__str__() + ", " + ws.cell(row=2, column=3).value.__str__() + ", 7\n")
for r in range(2,16000):
    if not ws.cell(row=r,column=1).value:
        break
    if not ws.cell(row=r, column=1).value == curStud:
        curStud = ws.cell(row=r, column=1).value
        file.write("\n" + curStud.__str__() + ", Student, " + curStud.__str__() + ", " + ws.cell(row=r, column=3).value.__str__() + ", 7\n")
    if not ws.cell(row=r, column=5).value == "See Counselor":
        file.write(ws.cell(row=r,column=4).value.__str__()+"\n")
'''

curStud = 0
r = 2
# FINISH MODIFYING to count how many course requests each student has before printing to text file (store course requests in list)
while ws.cell(row=r, column=1):
    while ws.cell(row=r,column=1)==curStud:

