# Script used to calculate the number of unfulfillable requests in the 2017-2018 requests data
# Spreadsheets needed: 6-1-17@1430.xlsx and SecList 8-14@1300.xlsx

from openpyxl import load_workbook

stud_wb = load_workbook(filename="../../runs/constraint_files/6-1-17@1430.xlsx")
sec_wb = load_workbook(filename="../../runs/constraint_files/SecList 8-14@1300.xlsx")


sec_ws = sec_wb['D1BC6ACA-A78F-4688-9C6D-42D84ED']
stud_ws = stud_wb['Sheet1']

# FINISH EDITING THIS!
raise Exception("Finish collecting number of course requests per courseID")
while stud_ws.cell(row=r, column=1).value:
    courseRequests = {}
    if stud_ws.cell(row=r,column=5).value == "See Counselor":
        r+=1
        continue
    sectID = [stud_ws.cell(row=r, column=4).value.__str__()]
    if sectID == "503000":
        courseRequests.append("3190T1")
        courseRequests.append("313753")
    elif sectID == "505000":
        courseRequests.append("313754")
        courseRequests.append("316055")
    elif sectID == "501000":
        courseRequests.append("3190T1")
        courseRequests.append("314351")
    elif sectID == "502000":
        courseRequests.append("313753")
        courseRequests.append("313754")
    elif sectID == "504000":
        courseRequests.append("3190T1")
        courseRequests.append("313754")
    elif sectID == "231904":
        courseRequests.append("231905")
    elif sectID == "2340T1":
        courseRequests.append("234093")
    else:
        courseRequests.append(stud_ws.cell(row=r, column=4).value.__str__())
    r += 1
    file.write(curStud.__str__() + ", Student, " + curStud.__str__() + ", " + stud_ws.cell(row=r-1, column=3).value.__str__() + ", " + len(courseRequests).__str__() + "\n")
    for x in range(len(courseRequests)):
        file.write(courseRequests[x] + "\n")
    file.write("\n")
    #print(curStud)
    #print(courseRequests)
    curStud = stud_ws.cell(row=r, column=1).value

# Gets totals for space in 
for r in range()