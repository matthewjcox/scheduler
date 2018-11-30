import re

'''
file = open("/Users/SarahGold/Documents/School/SysLab/20181017/coursesHtml.txt", "r")
newFile = open("/Users/SarahGold/Documents/School/SysLab/20181017/courseHtmlMinus<>.txt", "w")
temp = re.sub(r'<.*?>', "", file.read())
newFile.write(re.sub(r'&amp;', "&", temp))
'''

file = open("/Users/SarahGold/Documents/School/SysLab/20181017/courseHtmlMinus<>.txt", "r")
newFile = open("/Users/SarahGold/Documents/School/SysLab/20181017/newCourses.txt", "w")
courses = {}
x = 0
for line in file.read().splitlines():
    if re.match(r'\t{5}[^\t]', line) and not re.search('Frequently Asked Questions', line):
        x += 1
        #newFile.write(line[5:])
        #newFile.write("\n")
        if x == 1:
            curCourse = line[5:]
            courses[curCourse] = [curCourse] + ["" for x in range(3)]
        elif x == 2:
            courses[curCourse][2] = line[5:]
        elif x == 3:
            if line[5:] == "1.0":
                courses[curCourse][3] = "year"
            else:
                courses[curCourse][3] = "semester"
        elif x == 5:
            courses[curCourse][1] = line[5:]
        if x >= 6:
            x = 0
            print(courses[curCourse])
            #newFile.write("\n")
for course in courses.keys():
    newFile.write(", ".join(courses[course]))
    newFile.write("\n")


