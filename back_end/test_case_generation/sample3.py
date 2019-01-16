import random
'''
So we want a class of 400.
Math:
    80% take Research and Statistics 1
    10% take TJ Math 3
    5% take TJ Math 5
    2.5% take TJ Math 4
    2.5% take AP Calculus AB
    mathDist = {"TJ Res Stats 1":0.8, "TJ Math 3":0.1, "TJ Math 5":0.05, "TJ Math 4":0.025, "AP Calculus AB":0.025}
Biology:
    100% take Biology 1
    bioDist = {"Biology 1":1}
English:
    100% take English 9
    engDist = {"English 9":1}
Tech:
    100% take Design and Technology
    techDist = {"Design and Tech":1}
Language:
    25% take Latin 2
    20% take French 2
    40% take Spanish 2
    2.5% take Japanese 1
    5% take Chinese 1
    2.5% take Russian 1
    5% take German 1
    langDist = {"Latin 2":0.25, "French 2":0.20, "Spansih 2":0.4, "Japanese 1":0.025, "Chinese 1":0.05, "Russian 1":0.025, "German 1":0.05}
Gym:
    100% take Gym
    gymDist = {"Health and PE 9":1}
Elective:
    70% take Foundations of Computer Science
    10% take Foundations of Computer Science Accelerated
    5% take Symphonic Band
    5% take AP Computer Science
    5% take Advanced Orchestra
    2.5% take Theatre Arts 1
    2.5% take Art
    electDist = {"Foundations CompSci":0.7, "Foundations CompSci Acc":0.1, "Symphonic Band":0.05, "AP Computer Sci A+":0.05, "Advanced Orchestra":0.05, "Theatre Arts 1":0.025, "Art 1":0.025}
'''
numStuds = 400

students = {x:[] for x in range(numStuds)}
courseToNumber = {line.split(", ")[1]:line.split(", ")[2] for line in open("courses.txt", "r").read().splitlines()}
print(courseToNumber)

mathDist = {"TJ Res Stats 1":0.8, "TJ Math 3":0.1, "TJ Math 5":0.05, "TJ Math 4":0.025, "AP Calculus AB":0.025}
bioDist = {"Biology 1":1}
engDist = {"English 9":1}
techDist = {"Design and Tech":1}
langDist = {"Latin 2":0.25, "French 2":0.20, "Spanish 2":0.4, "Japanese 1":0.025, "Chinese 1":0.05, "Russian 1":0.025, "German 1":0.05}
gymDist = {"Health and PE 9":1}
electDist = {"Foundations CompSci": 0.7, "Foundations CompSci Acc": 0.1, "Symphonic Band": 0.05, "AP Computer Sci A+": 0.05, "Advanced Orchestra": 0.05, "Theatre Arts 1": 0.025, "Art 1": 0.025}

def removeStuds(baseSet, toRemove):
    return baseSet.difference({*toRemove})

def assignStudents(dist):
    studs = {x for x in range(numStuds)}
    for course in dist.keys():
        toRemove = set()
        for stud in random.sample(studs, int(dist[course]*numStuds)):
            students[stud].append(courseToNumber[course])
            toRemove.add(stud)
        studs = studs.difference(toRemove)

def writeStuds():
    file = open("sample_3_students.txt", "w")
    for student in students.keys():
        toAdd = student.__str__() + ", Student, " + student.__str__() + ", 7\n"
        file.write(toAdd)
        for course in students[student]:
            file.write(course + "\n")
        file.write("\n")


assignStudents(mathDist)
assignStudents(bioDist)
assignStudents(engDist)
assignStudents(techDist)
assignStudents(langDist)
assignStudents(gymDist)
assignStudents(electDist)
writeStuds()

# Math
'''
mathStuds = {x for x in range(numStuds)}
rs1 = random.sample(mathStuds, int(0.8*numStuds))
mathStuds = removeStuds(mathStuds, rs1)
math3 = random.sample(mathStuds, int(0.1*numStuds))
mathStuds = removeStuds(mathStuds, math3)
math5 = random.sample(mathStuds, int(.05*numStuds))
mathStuds = removeStuds(mathStuds, math5)
math4 = random.sample(mathStuds, int(0.025*numStuds))
mathStuds = removeStuds(mathStuds, math4)
abCalc = random.sample(mathStuds, int(0.025*numStuds))
mathStuds = removeStuds(mathStuds, abCalc)
for stud in rs1:
    students[stud].append(courseToNumber["TJ Res Stats 1"])
for stud in math3:
    students[stud].append(courseToNumber["TJ Math 3"])
for stud in math4:
    students[stud].append(courseToNumber["TJ Math 4"])
for stud in math5:
    students[stud].append(courseToNumber["TJ Math 5"])
for stud in abCalc:
    students[stud].append(courseToNumber["AP Calculus BC"])
'''

