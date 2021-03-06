from basics import *

def set_attribute(s,field,value,sections,classrooms,courses,teachers,students):
    if field == 'teacher':
        v = teachers[value]
        s.add_teacher(v)
    elif field == 'student':
        v = students[value]
        s.add_student_basic(v)
    elif field == 'courseID':
        v = courses[value]
        s.set_course(v)
    elif field == 'room':
        v = classrooms[value]
        s.add_classroom(v)
    elif field == 'team' or field=='team_1' or field=='team1':
        v = sections[value]
        s.team_1(v)
    elif field=='team_2' or field=='team2':
        v = sections[value]
        s.team_2(v)
    elif field=='team_3' or field=='team3':
        v = sections[value]
        s.team_3(v)
    elif field == 'period':
        v = int(value)
        s.set_period(v)
        s.fix_period()
    elif field == 'semester':
        v = int(value)
        s.set_semester(v)
    elif field == 'maxstudents':
        v = int(value)
        s.set_max_students(v+1)
    elif field == 'minstudents':
        v = int(value)
        s.set_min_students(v)
    elif field == 'allowed_periods':
        v=[int(i.strip()) for i in value.split(',')]
        s.set_allowed_periods(v)
    elif field=="same_periods":
        raise NotImplementedError
    else:
        print('Error entering data for section {}: no attribute {}'.format(s.id,field))
        raise ReferenceError

def read_classrooms(classroom_fn,classrooms):
    with open(classroom_fn, 'r') as f:
        for i in f:
            num=i.strip()
            classrooms[num]=Classroom.classroom(num)

def read_courses(course_fn,courses):
    with open(course_fn, 'r') as f:
        for i in f:
            line = [j.strip() for j in i.split('|')]
            try:
                course = Course.create_new(*line)
            except:
                print('Error reading course: '+line)
                raise
            courses[course.courseID] = course


def read_teachers(teacherfn,teachers):
    with open(teacherfn, 'r') as f:
        data=f.readlines()
        i=0
        for i in range(len(data)):
            try:
                teacherinfo=data[i].strip()
                if len(teacherinfo)==0:
                    continue
                fn,ln,teacher_id=teacherinfo.split(',')
                fn=fn.strip()
                ln=ln.strip()
                teacher_id=teacher_id.strip()
                tchr=Teacher(ln, fn, teacher_id, None)
                teachers[teacher_id]=tchr
            except IndexError as e:
                print(e)
                raise




def read_students(studentfn,students,all_courses):
    with open(studentfn, 'r') as f:
        data=f.readlines()
        i=0
        while i<len(data):
            try:
                studentinfo=data[i].strip()
                i+=1
                # print(studentinfo)
                id,fn,ln,grade,num_classes=studentinfo.split(',')
                id=id.strip()
                fn = fn.strip()
                ln = ln.strip()
                grade=grade.strip()
                num_classes = int(num_classes)
                classes=[]
                for j in range(num_classes):
                    classes.append(data[i+j].strip())
                try:
                    courses=Student_Courses(classes,all_courses)
                except:
                    print(id)
                    raise
                stud=Student(ln, fn, id, grade, courses)
                students[id]=stud
                i += num_classes+1
            except IndexError as e:
                print(e)
                raise

# def read_student_teaming(studentteamfn,students,all_courses):
#     with open(studentteamfn, 'r') as f:
#         data = f.readlines()
#         i = 0
#         while i < len(data):
#             try:
#                 courseid,num_students = [i.strip() for i in data[i].split(' ')]
#                 i += 1
#                 course=all_courses[courseid]
#                 num_students=int(num_students)
#                 stud0=None
#                 for j in range(num_students):
#                     if stud0 is None:
#                         stud0=students[data[i+j].strip()]
#                     else:
#                         stud=students[data[i+j].strip()]
#                         stud0.team(course,stud)
#                 i += num_students + 1
#             except IndexError as e:
#                 print(e)
#                 raise


def read_sections(sectionfn,sections,num_periods,classrooms,courses,teachers,students):
    with open(sectionfn, 'r') as f:#Read twice: first time, just get IDs, then second time, populate with teacher, periods, etc. Necessary in order to allow teaming cross-referencing.
        lines=f.readlines()
        j=0
        try:
            while j<len(lines):
                i = lines[j].strip()
                j+=1
                if not i:
                    continue
                if i in sections:
                    s=sections[i]
                else:
                    s=Section(i)
                    sections[i]=s
                i = lines[j].strip()
                j+=1
                while i:
                    field,value=i.split(':')
                    field=field.strip()
                    value=value.strip()
                    # set_attribute(s,field,value,sections,classrooms,courses,teachers,students)
                    i = lines[j].strip()
                    j+=1
        except IndexError as e:
            print(e)
            raise
        j = 0
        try:
            while j < len(lines):
                i = lines[j].strip()
                j += 1
                if not i:
                    continue
                if i in sections:
                    s = sections[i]
                else:
                    s = Section(i)
                    sections[i] = s
                i = lines[j].strip()
                j += 1
                while i:
                    field, value = i.split(':')
                    field = field.strip()
                    value = value.strip()
                    set_attribute(s, field, value, sections, classrooms, courses, teachers, students)
                    i = lines[j].strip()
                    j += 1
        except IndexError as e:
            print(e)
            raise
