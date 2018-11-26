from genetic_algorithm import *

teacher_input='sample_3_teachers.txt'
student_input='sample_3_students.txt'
section_input='sample_3_sections.txt'
#
# teacher_input='teachers_copy.txt'
# student_input='students.txt'
# section_input='sections.txt'

def set_attribute(s,field,value):
    if field == 'teacher':
        v = School.teachers[value]
        s.add_teacher(v)
    elif field == 'student':
        v = School.students[value]
        s.add_student(v)
    elif field == 'courseID':
        v = School.courses[value]
        s.add_course(v)
    elif field == 'room':
        v = School.classrooms[value]
        s.add_classroom(v)
    elif field == 'team':
        v = School.sections[value]
        s.team_with(v)
    elif field == 'period':
        v = int(value)
        s.set_period(v)
        s.fix_period()
    elif field == 'semester':
        v = int(value)
        s.set_semester(v)
    elif field == 'maxstudents':
        v = int(value)
        s.set_max_students(v)
    elif field == 'allowed_periods':
        v=[int(i.strip()) for i in value.split(',')]
        s.set_allowed_periods(v)
    else:
        print(f'Error entering data for section {s.id}: no attribute {field}')
        raise ReferenceError

if __name__=="__main__":
    with open(teacher_input,'r') as f:
        data=f.readlines()
        i=0
        while 1:
            try:
                teacherinfo=data[i].strip()
                i += 1
                fn,ln,teacher_id=teacherinfo.split(',')
                fn=fn.strip()
                ln=ln.strip()
                teacher_id=teacher_id.strip()
                # periods_available=[int(j) for j in data[i].split(',')]
                Teacher(ln, fn, teacher_id, None)
                # i+=2
            except IndexError:
                break
    with open(section_input,'r') as f:
        lines=f.readlines()
        j=0
        try:
            while 1:
                i = lines[j].strip()
                j+=1
                if not i:
                    continue
                if i in School.sections:
                    s=School.sections[i]
                else:
                    s=Section(i)
                i = lines[j].strip()
                j+=1
                while i:
                    field,value=i.split(':')
                    field=field.strip()
                    value=value.strip()
                    set_attribute(s,field,value)
                    i = lines[j].strip()
                    j+=1
        except IndexError as e:
            print(e)
            pass


    with open(student_input,'r') as f:
        data=f.readlines()
        i=0
        while 1:
            try:
                studentinfo=data[i].strip()
                i+=1
                # print(studentinfo)
                id,fn,ln,num_classes=studentinfo.split(',')
                id=id.strip()
                fn = fn.strip()
                ln = ln.strip()
                num_classes = int(num_classes)
                classes=[]
                for j in range(num_classes):
                    classes.append(data[i+j].strip())
                courses=Student_Courses(classes)
                Student(ln, fn, id, courses)
                i += num_classes+1
            except IndexError:
                break

    # for i in School.teachers.values():
    #     print(i.long_string())
    # # for i in School.students.values():
    # #     print(i.long_string())
    # print("_______________________________________________________________________")
    # s=master_schedule()
    # s.fill_new()
    # s.sections['17'].set_period(3)
    # s.sections['17'].fix_period()
    # s.sections['17'].set_period(5)
    # for i in s.teachers.values():
    #     print(i.long_string())
    # for i in s.students.values():
    #     print(i.long_string())

    # time_func=time.process_time_ns
    # # time_func=time.perf_counter_ns
    # time_scale=1e9
    # for i in range(1):
    #     t=time_func()
    #     for i in range(100000):
    #         master_schedule().fill_new()
    #     print((time_func()-t)/time_scale)

    solver = hill_climb_solo_2(master_schedule)
    winner=solver.solve(num_iterations=100, verbose=0,print_every=5)
    initial_score=winner.score()
    winner=fill_in_schedule(winner)
    print(winner)
    # for i in winner.sections.values():
    #     print(i.long_string())
    #     print()
    with open('winning_schedule.txt','w') as f:
        for i in winner.sections.values():
            f.write(i.long_string())
            f.write('\n\n')
        for i in winner.students.values():
            f.write(str(i))
            f.write(i.medium_string())
            f.write('\n\n')
    print('Schedule was printed to winning_schedule.txt.')
    print(f'Initial score: {initial_score}')
    print(f'Score after processing: {winner.score()}')
