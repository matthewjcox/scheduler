from basics import *
from genetic_algorithm import *
from parse_constraints import *
import datetime
import sqlite3
import os
import shutil
import tkinter as tk
import threading

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

    solver = multiple_hill_climb(master_schedule,num_periods,classrooms,courses,teachers,students,sections,save)
    yield from solver.solve(verbose=0, print_every=1)

class Application:
    def __init__(self, root, master=None):
        self.master=master

        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)

        self.frame=tk.Frame(root)
        self.frame.master.title("Scheduler")
        self.frame.grid(row=0, column=0, sticky="nsew")
        # self.fr1.grid(column=0, row=0,sticky="nsew")
        # self.frame = tk.Frame(self.fr1)
        self.root=root
        self.root.minsize(400, 200)
        self.root.geometry("500x400")
        self.frame.grid(sticky=(tk.N,tk.W,tk.E,tk.S))
        self.running_state=0#0:stopped; 1:running; 2:stopping

        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=0)
        self.frame.rowconfigure(2, weight=0)
        self.frame.rowconfigure(3, weight=0)
        self.frame.rowconfigure(4, weight=0)
        self.frame.rowconfigure(5, weight=0)
        self.frame.rowconfigure(6, weight=1)
        self.frame.rowconfigure(7, weight=2)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.default_dir="Start from scratch"
        self.chosen_dir= tk.StringVar(self.root)
        dirs=[self.default_dir]+[name for name in os.listdir("runs/past_runs/") if os.path.isdir("runs/past_runs/"+name)][::-1]
        self.chosen_dir.set(dirs[0])

        self.dirchooser=tk.OptionMenu(self.frame,self.chosen_dir,*dirs)
        self.dirchooser.grid(row=0,column=1, sticky='w')
        self.dirchooserlabel=tk.Label(self.frame,text="Choose prior run to continue improving: ")
        self.dirchooserlabel.grid(row=0,column=0,sticky="e")
        self.statuslabel = tk.Label(self.frame, text="Status: ")
        self.statuslabel.grid(row=2, column=0, sticky="e")
        self.roundlabel = tk.Label(self.frame, text="Round: ")
        self.roundlabel.grid(row=3, column=0, sticky="e")
        self.scorelabel = tk.Label(self.frame, text="Completion: ")
        self.scorelabel.grid(row=4, column=0, sticky="e")
        self.timelabel = tk.Label(self.frame, text="Time elapsed: ")
        self.timelabel.grid(row=5, column=0, sticky="e")
        self.statusdisp = tk.Label(self.frame, text="Awaiting input")
        self.statusdisp.grid(row=2, column=1, sticky="w")
        self.rounddisp = tk.Label(self.frame, text="Awaiting input")
        self.rounddisp.grid(row=3, column=1, sticky="w")
        self.scoredisp = tk.Label(self.frame, text="Awaiting input")
        self.scoredisp.grid(row=4, column=1, sticky="w")
        self.timedisp = tk.Label(self.frame, text="Awaiting input")
        self.timedisp.grid(row=5, column=1, sticky="w")

        self.toggle_button = tk.Button(self.frame, text='\nStart Scheduling\n', background="#AAFFAA",activebackground="#AAEEAA", command=self.run_sched)
        self.toggle_button.grid(row=7, column=0,columnspan=2, sticky=(tk.N,tk.W,tk.E,tk.S))

    def full_exit(self):
        # self.quit()
        self.destroy()

    def run_sched(self):
        self.running=1
        self.toggle_button.config(text='\nStop Scheduling\n',background="#FFAAAA",activebackground="#EEAAAA", command=self.stop_sched)
        self.dirchooser.config(state='disabled')
        self.update_display("starting run")
        self.root.update()
        thr=threading.Thread(target=self.thread_sched_runner)
        thr.start()

        
    def thread_sched_runner(self):
        dir = self.chosen_dir.get()
        if dir == self.default_dir:
            dir = None
        runner = run_scheduler(save=dir)
        while 1:
            if self.running==1:
                data=runner.send(None)
                self.update_display(data)
                self.root.update()
                runner.send(None)
            elif self.running==2:
                try:
                    runner.send(None)
                    runner.send(1)
                except StopIteration:
                    pass
                break
        self.sched_stopped()

    def update_display(self,data):
        if data == "starting run":
            self.statusdisp.config(text="Run starting")
        elif data=="no run":
            self.statusdisp.config(text="Awaiting input")
            self.rounddisp.config(text="Awaiting input")
            self.scoredisp.config(text="Awaiting input")
            self.timedisp.config(text="Awaiting input")
        else:
            score,maxscore,it,time=data
            self.statusdisp.config(text="Running")
            self.rounddisp.config(text="{}".format(it))
            self.scoredisp.config(text="{:.3f}%".format(score/maxscore*100))
            self.timedisp.config(text="{}".format(time))


    def sched_stopped(self):
        self.running = 0
        self.toggle_button.config(text='\nStart Scheduling\n', background="#AAFFAA", activebackground="#AAEEAA",command=self.run_sched,state="normal")
        self.update_display("no run")

    def stop_sched(self):
        self.running = 2
        self.toggle_button.config(text='\nStopping ...\n')


def main():
    root=tk.Tk()
    app = Application(root)
    app.frame.mainloop()
    # run_scheduler(save=None)#"2019_02_25__19_27_42")#"2019_02_22__18_12_46")#"2019_01_16__20_53_43")


if __name__=="__main__":
    main()
