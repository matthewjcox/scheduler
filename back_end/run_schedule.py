from basics import *
from genetic_algorithm import *
from parse_constraints import *
import datetime
import sqlite3
import os
import shutil
from tendo import singleton
lock=singleton.SingleInstance()

lock_failed=0
class LockError(Exception):
    pass
def run_scheduler(save=None):
    if save is None:
        save='runs/past_runs/'+datetime.datetime.strftime(datetime.datetime.utcnow(),"%Y_%m_%d__%H_%M_%S")
        os.mkdir(save)
        start_logging(save)
        param_file_name = 'runs/run_params.txt'
        try:
            shutil.copy2(param_file_name,save)
        except TypeError:
            raise FileNotFoundError
        connection = sqlite3.connect(save+'/schedule.db')
        cursor=connection.cursor()
        cursor.execute("CREATE TABLE metadata(iteration int,time_elapsed real);")
        cursor.execute('INSERT INTO metadata(iteration,time_elapsed) VALUES (0,0)')
        connection.commit()
        connection.close()
    else:
        save='runs/past_runs/'+save
        start_logging(save)
        param_file_name = save+'/run_params.txt'
        connection = sqlite3.connect(save + '/schedule.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM metadata')
        it,time_el=cursor.fetchone()
        set_global_parameters(it,time_el)
        connection.commit()
        connection.close()
    with open(param_file_name, 'r') as f:
        num_periods,classroom_fn, course_fn, teacher_fn, student_fn, student_team_fn, section_fn=[i.strip() for i in f.readlines()]
    for i in classroom_fn, course_fn, teacher_fn, student_fn, student_team_fn, section_fn:
        if not os.path.isfile(save+'/'+i):
            try:
                shutil.copy2('runs/constraint_files/'+i, save)
            except TypeError:
                raise FileNotFoundError
    num_periods=int(num_periods.strip())
    set_global_num_periods(num_periods)
    classroom_fn, course_fn, teacher_fn, student_fn,student_team_fn, section_fn=[save+'/'+i for i in (classroom_fn, course_fn,  teacher_fn, student_fn,student_team_fn, section_fn)]
    classrooms={}
    courses={}
    teachers={}
    sections={}
    students={}
    read_classrooms(classroom_fn,classrooms)
    read_courses(course_fn,courses)
    read_teachers(teacher_fn,teachers)
    read_students(student_fn,students,courses)
    # read_student_teaming(student_team_fn,students,courses) #STUDENT TEAMING IS NOT YET FUNCTIONAL
    read_sections(section_fn, sections,num_periods,classrooms,courses,teachers,students)

    solver = hill_climb_solo_2(master_schedule,num_periods,classrooms,courses,teachers,students,sections,save)
    solver.solve(verbose=0, print_every=1)


def main():
    run_scheduler(save=None)#"2019_02_25__19_27_42")#"2019_02_22__18_12_46")#"2019_01_16__20_53_43")


if __name__=="__main__":
    main()
