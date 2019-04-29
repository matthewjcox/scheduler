from basics import *
from genetic_algorithm import *
from parse_constraints import *
import datetime
import sqlite3
import os
import shutil
import tkinter as tk

# from tendo import singleton
# lock=singleton.SingleInstance()

lock_failed=0
class LockError(Exception):
    pass
def run_scheduler(save=None):
    if len(sys.argv)>1:
        try:
            set_global_num_cores(int(sys.argv[1]))#Default: 8
        except TypeError:
            pass
    if save is None:
        save='[name for name in os.listdir(".") if os.path.isdir(name)]'+datetime.datetime.strftime(datetime.datetime.utcnow(),"%Y_%m_%d__%H_%M_%S")
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

    solver = multiple_hill_climb(master_schedule,num_periods,classrooms,courses,teachers,students,sections,save)
    solver.solve(verbose=0, print_every=1)

class Application(tk.Frame):
    def __init__(self, root, master=None):
        self.root=root
        self.root.minsize(300, 300)
        self.root.geometry("800x600+300+300")
        tk.Frame.__init__(self, master)
        self.grid(sticky="nwse")
        self.createWidgets()

    def createWidgets(self):
        # top = self.winfo_toplevel()
        # top.rowconfigure(0, weight=1)
        # top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        dirs=["Start from scratch"]+[name for name in os.listdir("runs/past_runs/") if os.path.isdir("runs/past_runs/"+name)][::-1]
        print(dirs)

        self.start_button = tk.Button(self, text='Start Schedule', background="#AAFFAA",activebackground="#AAEEAA", command=self.run_sched)
        self.start_button.grid(row=0, column=0, sticky="nsew")

    def full_exit(self):
        # self.quit()
        self.destroy()

    def run_sched(self):
        self.full_exit()
        pass


def main():
    root=tk.Tk()
    app = Application(root)
    app.master.title('Scheduler')
    app.mainloop()
    # run_scheduler(save=None)#"2019_02_25__19_27_42")#"2019_02_22__18_12_46")#"2019_01_16__20_53_43")


if __name__=="__main__":
    main()
