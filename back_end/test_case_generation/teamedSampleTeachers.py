import random
import re

teachers = {}
teachers["James"] = "Jennifer, James, jjames1"
teachers["Larson"] = "Thomas, Larson, tglarson"
teachers["Holman"] = "Aubrie, Holman, asholman"
teachers["Del Cerro"] = "Sonia, Del Cerro, sdelcerro"
#teachers["Rosenblum"] = "Jennifer, Rosenblum, jmrosenblum" #Now Fisher

teachers["Kochman"] = "Mary, Kochman, mbkochman"
teachers["Glover"] = "Nancy, Glover, neglover"
teachers["Harris"] = "Erinn, Harris, eharris1"
teachers["Glotfelty"] = "Stephanie, Glotfelty, slglotfelty"
#teachers["Miller"] = "Michael, Miller, mhmiller2"

teachers["James1"] = "Jeffrey, James, jcjames"
teachers["Potoker"] = "Barry, Potoker, bnpotoker"
teachers["Smith"] = "Heidi, Smith, hesmith"

teachers["Lewis"] = "Craig, Lewis, calewis1"
teachers["Jones"] = "Darcie, Jones, djones3"
teachers["Geiger"] = "Monica, Geiger, mggeiger"
teachers["Seyler"] = "Jared, Seyler, jcseyler"
#teachers["Piccone"] = "Michael, Piccione, mspiccione"

teachers["Kim"] = "Nicole, Kim, njkim"
teachers["Eckel"] = "Malcolm, Eckel, mceckel"
teachers["Rose"] = "Stephen, Rose, srrose"
teachers["Billington"] = "Marion, Billington, mlbillington"
teachers["Lister"] = "Patricia, Lister, phlister"
teachers["Conklin"] = "Christine, Conklin, clconklin"
teachers["Van de Kamp"] = "Cynthia, Van de Kamp, cvandekampwa"
teachers["Gendive"] = "Margaret, Gendive, magendive"
teachers["Mateo"] = "Nannette, Mateo, nmateo"
teachers["Oszko"] = "Szilvia, Oszko, soszko"
teachers["Sandstrom"] = "Elizabeth, Sandstrom, ecsandstrom"
teachers["Xu"] = "Qin, Xu, qxu1"
teachers["Otani"] = "Koji, Otani, kotani"
teachers["Foreman"] = "Adam, Foreman, awforeman"
teachers["Bailey"] = "Allison, Bailey, akbailey"
teachers["Reid"] = "Andrew, Reid, amreid"
teachers["Davis"] = "Timothy, Davis, tadavis2"
teachers["Hill"] = "David, Hill, dlhill2"
teachers["Carey"] = "Isaac, Carey, ijcarey"
teachers["Lampazzi"] = "Amy, Lampazzi, anlampazzi"
teachers["Jirari-Scavotto"] = "Alouf, Jirari-Scavotto, ajirariscavo"
teachers["Lightner"] = "Corey, Lightner, cllightner"


courseToTeacher = {}
courseToTeacher["Biology 1"] = ["James", "Larson", "Holman", "Del Cerro"] #, "Rosenblum"]
courseToTeacher["English 9"] = ["Kochman", "Glover", "Harris", "Glotfelty"] #, "Miller"]
courseToTeacher["Health and PE 9"] = ["James1", "Potoker", "Smith"]
courseToTeacher["Design and Tech"] = ["Lewis", "Jones", "Geiger", "Seyler"] #, "Piccone"]
courseToTeacher["Foundations CompSci"] = ["Kim", "Eckel", "Rose", "Billington"]
courseToTeacher["Foundations CompSci Acc"] = courseToTeacher["Foundations CompSci"]
courseToTeacher["AP Computer Sci A+"] = courseToTeacher["Foundations CompSci"]
courseToTeacher["Latin 2"] = ["Lister", "Conklin"]
courseToTeacher["French 2"] = ["Van de Kamp"]
courseToTeacher["Spanish 2"] = ["Gendive", "Mateo"]
courseToTeacher["German 1"] = ["Oszko"]
courseToTeacher["Russian 1"] = ["Sandstrom"]
courseToTeacher["Chinese 1"] = ["Xu"]
courseToTeacher["Japanese 1"] = ["Otani"]
courseToTeacher["Symphonic Band"] = ["Foreman"]
courseToTeacher["Advanced Orchestra"] = ["Bailey"]
courseToTeacher["Theatre Arts 1"] = ["Reid"]
courseToTeacher["Art 1"] = ["Davis"]
courseToTeacher["TJ Res Stats 1"] = ["Hill", "Carey", "Lampazzi", "Jirari-Scavotto", "Lightner"]
courseToTeacher["TJ Math 3"] = courseToTeacher["TJ Res Stats 1"]
courseToTeacher["TJ Math 4"] = courseToTeacher["TJ Res Stats 1"]
courseToTeacher["TJ Math 5"] = courseToTeacher["TJ Res Stats 1"]
courseToTeacher["AP Calculus AB"] = courseToTeacher["TJ Res Stats 1"]

courseToSections = {"TJ Res Stats 1":17, "TJ Math 3":17, "TJ Math 5":2, "TJ Math 4":2, "AP Calculus AB":1, "Biology 1":24, "English 9":24, "Design and Tech":24, "Latin 2":6, "French 2":5, "Spanish 2":9, "Japanese 1":1, "Chinese 1":1, "Russian 1":1, "German 1":1, "Health and PE 9":11, "Foundations CompSci":14, "Foundations CompSci Acc":3, "Symphonic Band":1, "AP Computer Sci A+":1, "Advanced Orchestra":1, "Theatre Arts 1":1, "Art 1":1}
print(sum(v for v in courseToSections.values()))

courseToNumber = {line.split("| ")[1]:[line.split("| ")[2], line.split("| ")[3]] for line in open("../../runs/constraint_files/newCourses.txt", "r").read().splitlines()}
numberToCourse = {line.split("| ")[2]:[line.split("| ")[1], line.split("| ")[3]] for line in open("../../runs/constraint_files/newCourses.txt", "r").read().splitlines()}

teacherToSection = {}
sections = {}
secID = 100000

#team: [sectionID]
#allowed_periods: 1,2,3,4 (space separated or not)

def assignSections():
    global secID
    print("assignSections")
    # FIND WHERE THIS IS GETTING STUCK IN A LOOP!!!
    x = 0
    for course in courseToSections.keys():
        x += 1
        print("Course: " + course + ", " + x.__str__())
        # Adjustment so that IBET teachers all get six courses. (Adjust to three or six?)
        if course in {"Biology 1", "English 9", "Design and Tech"}:
            t = int(int(courseToSections[course])/6)
            for k in range(t):
                teacher = random.choice(courseToTeacher[course])
                while teacher in teacherToSection.keys() and len(teacherToSection[teacher]) >=6:
                    teacher = random.choice(courseToTeacher[course])
                if not teacher in teacherToSection.keys():
                    teacherToSection[teacher] = []
                for y in range(3):
                    sections[secID] = [secID.__str__(), "teacher: "+teachers[teacher].split(", ")[2], "courseID: "+courseToNumber[course][0], "room: ?", "semester: 0","maxstudents: 20", "allowed_periods: 1,2,3"]
                    teacherToSection[teacher].append(secID)
                    secID += 1
                for y in range(3):
                    sections[secID] = [secID.__str__(), "teacher: " + teachers[teacher].split(", ")[2], "courseID: " + courseToNumber[course][0], "room: ?", "semester: 0", "maxstudents: 20", "allowed_periods: 5,6,7"]
                    teacherToSection[teacher].append(secID)
                    secID += 1
        else:
            for y in range(courseToSections[course]):
                teacher = random.choice(courseToTeacher[course])
                r = 5
                if not teacher in teacherToSection.keys():
                    teacherToSection[teacher] = []
                for c in teacherToSection[teacher]:
                    if numberToCourse[re.search(r'[A-Z]*[0-9]+[A-Z]*[0-9]*', sections[c][2]).group(0)][1] == "semester":
                        r += 1
                while teacher in teacherToSection.keys() and len(teacherToSection[teacher]) >= r:
                    teacher = random.choice(courseToTeacher[course])
                    if not teacher in teacherToSection.keys():
                        teacherToSection[teacher] = []
                    r = 5
                    sem = 0
                    for c in teacherToSection[teacher]:
                        if numberToCourse[re.search(r'[A-Z]*[0-9]+[A-Z]*[0-9]*', sections[c][2]).group(0)][1] == "semester":
                            sem += 1
                    if sem%2 == 1:
                        sem += 1
                    r += sem/2
                    #print("Hi")
                sections[secID] = [secID.__str__(), "teacher: "+teachers[teacher].split(", ")[2], "courseID: "+courseToNumber[course][0], "room: ?"]
                if course in {"TJ Res Stats 1", "TJ Math 4"}:
                    sections[secID].append("semester: 1")
                elif course in {"TJ Math 3", "TJ Math 5"}:
                    sections[secID].append("semester: 2")
                else:
                    sections[secID].append("semester: 0")
                if course == "Health and PE 9":
                    sections[secID].append("maxstudents: 40")
                else:
                    sections[secID].append("maxstudents: 20")
                teacherToSection[teacher].append(secID)
                secID += 1

# Teams IBETs by teams listed in function. Teaming info is stored under the bio teachers'
def teamSections():
    teams = [["James", "Kochman", "Lewis"], ["Larson", "Glover", "Jones"], ["Holman", "Harris", "Geiger"], ["Del Cerro", "Glotfelty", "Seyler"]]
    for team in teams:
        for x in range(6):
            sections[teacherToSection[team[0]][x]].append("team: " + teacherToSection[team[1]][x].__str__())
            sections[teacherToSection[team[0]][x]].append("team: " + teacherToSection[team[2]][x].__str__())

def writeSections():
    global secID
    print("writeSections")
    teamed = []
    sectionFile = open("../../runs/constraint_files/teamed_4_sections.txt", "w")
    for teacher in teacherToSection.keys():
        for section in teacherToSection[teacher]:
            sectionFile.write("\n".join(sections[section][:6]))
            if len(sections[section]) > 6:
                sectionFile.write("\n")
                sectionFile.write(sections[section][6])
            sectionFile.write("\n\n")
            if len(sections[section]) > 7:
                teamed.append(section)
    # Add meeting periods for teachers who teach the same subject(s)
    toAdd = secID.__str__() + "\nteacher: ".join(['']+[teachers[i].split(", ")[2] for i in courseToTeacher["Biology 1"]])+"\ncourseID: 000BIO\nroom: ?\nsemester: 0\nmaxstudents: 0\n\n"
    sectionFile.write(toAdd)
    secID += 1
    toAdd = secID.__str__() +"\nteacher: ".join(['']+[teachers[i].split(", ")[2] for i in courseToTeacher["English 9"]]) + "\ncourseID: 000ENG\nroom: ?\nsemester: 0\nmaxstudents: 0\n\n"
    sectionFile.write(toAdd)
    secID += 1
    toAdd = secID.__str__() + "\nteacher: ".join(['']+[teachers[i].split(", ")[2] for i in courseToTeacher["Health and PE 9"]]) + "\ncourseID: 000GYM\nroom: ?\nsemester: 0\nmaxstudents: 0\n\n"
    sectionFile.write(toAdd)
    secID += 1
    toAdd = secID.__str__() + "\nteacher: ".join(['']+[teachers[i].split(", ")[2] for i in courseToTeacher["Design and Tech"]]) + "\ncourseID: 000D&T\nroom: ?\nsemester: 0\nmaxstudents: 0\n\n"
    sectionFile.write(toAdd)
    secID += 1
    toAdd = secID.__str__() + "\nteacher: ".join(['']+[teachers[i].split(", ")[2] for i in courseToTeacher["Foundations CompSci Acc"]]) + "\ncourseID: 0000CS\nroom: ?\nsemester: 0\nmaxstudents: 0\n\n"
    sectionFile.write(toAdd)
    secID += 1
    toAdd = secID.__str__() + "\nteacher: ".join(['']+[teachers[i].split(", ")[2] for i in courseToTeacher["TJ Math 3"]]) + "\ncourseID: 000MAT\nroom: ?\nsemester: 0\nmaxstudents: 0\n\n"
    sectionFile.write(toAdd)
    secID += 1
    # Re-access teamed courses to add the teaming
    for sect in teamed:
        abridged = sections[sect][:1] + sections[sect][7:]
        sectionFile.write("\n".join(abridged))
        sectionFile.write("\n\n")


def writeTeachers():
    print("writeTeachers")
    teacherFile = open("../../runs/constraint_files/teamed_4_teachers.txt", "w")
    for teacher in teacherToSection.keys():
        toAdd = teachers[teacher] + "\n"
        teacherFile.write(toAdd)

assignSections()
teamSections()
writeSections()
writeTeachers()