import re

# NOTE: THIS FILE WILL NOT WORK ON GIT. Uses pathways for Sarah's laptop.


file = open("Course_Catalog_html.txt", "r")
tempfile = open("Course_Catalog_html_minus_tags.txt", "w")
temp = re.sub(r'<.*?>', "", file.read())
tempfile.write(re.sub(r'&amp;', "&", temp))

file.close()
tempfile.close()


file = open("Course_Catalog_html_minus_tags.txt", "r")
newFile = open("CourseList.txt", "w")
courses = {}
x = 0
for line in file.read().splitlines():
    if re.match(r'\t{5}[^\t]', line) and not re.search('Frequently Asked Questions', line):
        x += 1
        #newFile.write(line[5:])
        #newFile.write("\n")
        if x == 1:
            curCourse = line[5:]
            courses[curCourse] = [curCourse] + ["" for x in range(4)]#full name
        elif x == 2:
            courses[curCourse][2] = line[5:]#id
        elif x == 3:
            courses[curCourse][3] = line[5:]#semester
        elif x == 4:
            course[curCourse][4] = line[5:]#honors
        elif x == 5:
            courses[curCourse][1] = line[5:]#short name
        if x >= 6:
            x = 0
            print(courses[curCourse])
            #newFile.write("\n")
for course in courses.keys():
    newFile.write("| ".join(courses[course]))
    newFile.write("\n")
#'''

