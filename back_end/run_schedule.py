from basics import *
from genetic_algorithm import *
from parse_constraints import *
import datetime
import sqlite3
import os
import shutil

def run_scheduler(save=None):
    if save is None:
        save=f'runs/past_runs/{datetime.datetime.strftime(datetime.datetime.utcnow(),"%Y_%m_%d__%H_%M_%S")}'
        os.mkdir(save)
        param_file_name = 'runs/run_params.txt'
        shutil.copy2(param_file_name,save)
        connection = sqlite3.connect(save+'/schedule.db')
        cursor=connection.cursor()
        connection.commit()
        connection.close()
    else:
        save='runs/past_runs/'+save
        param_file_name = save+'/run_params.txt'
    with open(param_file_name, 'r') as f:
        num_periods,classroom_fn, course_fn, teacher_fn, student_fn, section_fn=[i.strip() for i in f.readlines()]
    for i in classroom_fn, course_fn, teacher_fn, student_fn, section_fn:
        if not os.path.isfile(f'{save}/{i}'):
            shutil.copy2('runs/constraint_files/'+i, save)
    num_periods=int(num_periods.strip())
    set_global_num_periods(num_periods)
    classroom_fn, course_fn, teacher_fn, student_fn, section_fn=[f'{save}/{i}' for i in (classroom_fn, course_fn,  teacher_fn, student_fn, section_fn)]
    classrooms={}
    courses={}
    teachers={}
    sections={}
    students={}
    read_classrooms(classroom_fn,classrooms)
    read_courses(course_fn,courses)
    read_teachers(teacher_fn,teachers)
    read_students(student_fn,students,courses)
    read_sections(section_fn, sections,num_periods,classrooms,courses,teachers,students)

    solver = hill_climb_solo_2(master_schedule,num_periods,classrooms,courses,teachers,students,sections,save)
    winner = solver.solve(num_iterations=1000, verbose=0, print_every=5)
    # initial_score = winner.score()

    # print(f'Schedule was printed to {filename}.')
    # print(f'Initial score: {initial_score}')
    # print(f'Score after processing: {winner.score()}')
    #allow for quit at any time?



if __name__=="__main__":
    run_scheduler(save="2018_12_07__18_52_41")
