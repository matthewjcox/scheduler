from basics import *
import random
import time
import sqlite3

_ITERATION=0
_START_TIME=time.perf_counter()
_SAVE_TIME=10
_CLOSENESS_TO_COMPLETION=0

def set_global_parameters(iteration,time_el):
    global _ITERATION
    global _START_TIME
    _ITERATION=iteration
    _START_TIME-=time_el



class NotImplemented(Exception):
    pass
class InvalidPeriodError(Exception):
    pass
class UnviableScheduleError(Exception):
    pass
class chromosome:
    def __init__(self,*args,**kwargs):
        pass

    def randomize_new(self):
        raise NotImplemented

    def mutate(self):
        raise NotImplemented

    def score(self):
        raise NotImplemented

    def weighted_score(self):
        raise NotImplemented

    def is_viable(self):
        raise NotImplemented

    @staticmethod
    def breed(a,b):
        raise NotImplemented

    def __str__(self):
        return '{} object, score={}'.format(self.__class__.__name__,self.score())



def weighted_choice(elements,n,weights):
    assert .999<=sum(weights)<=1.001
    res=[]
    for i in range(n):
        r=random.random()
        s=0
        for k,j in enumerate(weights):
            if s+j>r:
                break
            s+=j
        res.append(elements[k])
        weights[n]=0
        weights*=1-n
    return res


class master_schedule(chromosome):
    #criteria, data structures
    def __init__(self,num_periods,classrooms,courses,teachers,students,sections,*args,**kwargs):
        super(master_schedule, self).__init__(*args, **kwargs)
        self.num_periods=num_periods
        self.stock_classrooms=classrooms
        self.stock_courses=courses
        self.stock_teachers=teachers
        self.stock_students=students
        self.stock_sections=sections
        self.sections={}
        self.initialized = 0
        self.course_sections = {}


    def blank_new(self):
        pass

    def fill_new(self,fill_sections=1):
        self.teachers={}
        self.students={}
        self.classrooms={}
        for i in self.stock_teachers.values():
            self.teachers[i.teacherID]=i.copy()
        for i in self.stock_students.values():
            self.students[i.studentID]=i.copy()
        for i in self.stock_classrooms.values():
            self.classrooms[i.num]=Classroom(i.num)
        self.teams1=[]
        self.teams2 = []
        self.teams3 = []
        self.initialized=1
        if fill_sections:
            for i in self.stock_sections.values():
                s=Section(i.id)
                self.sections[s.id]=s
                for j in i.teachers:
                    teacher=self.teachers[j.teacherID]
                    s.add_teacher(teacher)
                for j in i.students:
                    student=self.students[j.studentID]
                    s.add_student_basic(student)
                for j in i.classrooms:
                    classroom=self.classrooms[j.num]
                    s.add_classroom(classroom)
                course=self.stock_courses[i.course.courseID]
                s.set_course(course)
                s.set_semester(i.semester)
                s.set_max_students(i.maxstudents)
                s.set_period(i.period)
                if i.period_fixed:
                    s.fix_period()
                s.set_allowed_periods(i.allowed_periods)
                for j in i.teamed1:
                    self.teams1.append((s,j.id))
                for j in i.teamed2:
                    self.teams2.append((s,j.id))
                for j in i.teamed3:
                    self.teams3.append((s,j.id))
            for sect in self.sections.values():
                course=sect.course
                if course not in self.course_sections:
                    self.course_sections[course] = []
                self.course_sections[course].append(sect)
            for i, j in self.teams1:
                other = self.sections[j]
                if other not in i.teamed1:
                    i.team_1(other)
            for i, j in self.teams2:
                other = self.sections[j]
                if other not in i.teamed2:
                    i.team_2(other)
            for i, j in self.teams3:
                other = self.sections[j]
                if other not in i.teamed3:
                    i.team_3(other)


    def retrieve_schedule(self,outfolder):
        self.fill_new()
        outfile = outfolder + '/schedule.db'
        connection = sqlite3.connect(outfile)
        cursor = connection.cursor()
        cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='schedule';")
        table_exists=cursor.fetchone()[0]
        print(table_exists)
        if table_exists:
            data=cursor.execute("SELECT * FROM schedule")
            for section,students,period in data:
                s=self.sections[section]
                s.set_period(int(period))
                for i in students.split('|'):
                    if i:
                        s.add_student_basic(self.students[i])
        else:
            pass#do nothing
        #DON'T COMMIT
        connection.close()

    def randomize_new(self):
        self.fill_new()


    def mutate_period(self,mutating_section=None,p=None,verbose=1,allow_randomness=0):
        if mutating_section is None:
            mutating_section,p=self.choose_mutating_section()
        if p is None:
            p = random.choice(mutating_section.allowed_periods)
        if verbose:
            print(repr(mutating_section),p)
        try:
            self.change_to_period(mutating_section, p, [],allow_randomness=allow_randomness)
        except InvalidPeriodError:
            pass


    def choose_mutating_section(self):
        period=None
        while 1:
            #Select a section:
            section=random.choice(tuple(self.sections.values()))
            if section.maxstudents==0:
                continue

            #Choose the new period for the section.
                #Avoid moving the section to a period in which the teacher is already teaching the same course:
            courses={}
            for i in section.teachers:
                for j in i.sched:
                    if j.period not in courses:
                        courses[j.period]=[]
                    courses[j.period].append(j.course)
            for i in sorted(section.allowed_periods,key=lambda i:random.random()):
                if i not in courses or not section.course in courses[i]:
                    period=i
                    break
            if period is not None:
                break

        return section,period

    def change_to_period(self, section, new_period, reached,allow_randomness=0):
        if new_period==section.period or section in reached:
            return
        if new_period not in section.allowed_periods:
            raise InvalidPeriodError
        reached.append(section)
        old_period=section.period
        section.set_period(new_period)
        try:
            for i in section.teachers:
                for j in i.sched:
                    if (section.semester==0 or j.semester==0 or section.semester==j.semester) and j not in section.teamed2:
                        if j.period==new_period:
                            self.change_to_period(j,random.choice(j.allowed_periods) if allow_randomness else old_period,reached)
            for j in section.teamed1:
                if j.period == new_period:
                    self.change_to_period(j, random.choice(j.allowed_periods) if allow_randomness else old_period, reached)
        except InvalidPeriodError:
            section.set_period(old_period)
            raise

    def initialize_weights(self):
        self.student_conflict_score_delta = -3
        self.teacher_conflict_score_delta = -10000
        self.correct_yr_course_score_delta = 4
        self.correct_sem_course_score_delta = 2
        self.theoretical_max_score=0
        for i in self.stock_students.values():
            for j in i.courses.courses:
                if j.duration=='year':
                    self.theoretical_max_score+=self.correct_yr_course_score_delta
                else:
                    self.theoretical_max_score+=self.correct_sem_course_score_delta
         # = self.correct_yr_course_score_delta * len(self.stock_students) * self.num_periods

        self.duplicate_correct_course_score_delta = -5
        self.rare_class_bonus = 20 * (1 - _CLOSENESS_TO_COMPLETION**2)
        self.section_in_prohibited_period_delta=-5000
        self.course_period_overlap=-10*(1-_CLOSENESS_TO_COMPLETION)**2

        self.section_exceeds_max_students_delta=-100

    def preliminary_score(self,static=0,verbose=0):
        if not self.initialized:
            raise ReferenceError
        score=0
        addl_score=0
        # self.initialize_weights()
        student_base_score=0
        student_addl_score=0
        student_conflict_score=0
        for i in self.students.values():
            student_score,_,conflicts=self.score_student(i)
            student_base_score+=_
            student_addl_score+=student_score-_
            student_conflict_score+=conflicts

        score+=student_base_score
        addl_score+=student_addl_score

        teacher_conflict_score=0
        for i in self.teachers.values():
            periods= {}
            for j in i.sched:
                k = j.period
                if k not in periods:
                    periods[k] = []
                same_period=periods[k]
                if j.semester == 0:
                    # k in periods_yr or k in periods_s1 or k in periods_s2:
                    for m in same_period:
                        if m not in j.teamed2:
                            teacher_conflict_score += self.teacher_conflict_score_delta
                            break
                    periods[k].append(j)
                elif j.semester == 1:
                    for m in same_period:
                        if m not in j.teamed2:
                            if m.semester==1 or m.semester==0:
                                teacher_conflict_score += self.teacher_conflict_score_delta
                                break
                    periods[k].append(j)
                elif j.semester == 2:
                    for m in same_period:
                        if m not in j.teamed2:
                            if m.semester==2 or m.semester==0:
                                teacher_conflict_score += self.teacher_conflict_score_delta
                                break
                    periods[k].append(j)
        score+=teacher_conflict_score

        period_spread_score=0
        for i in self.course_sections.values():
            period_counts={}
            for j in i:
                if j.period not in period_counts:
                    period_counts[j.period]=0
                period_counts[j.period]+=1
            for j in period_counts.values():
                if j>1:
                    period_spread_score+=j**2*self.course_period_overlap
        addl_score+=period_spread_score

        section_penalty_score=0
        for i in self.sections.values():
            if i.period not in i.allowed_periods:
                section_penalty_score+=self.section_in_prohibited_period_delta
        for i in self.sections.values():
            if len(i.students)>i.maxstudents:
                section_penalty_score+=self.section_exceeds_max_students_delta
        score+=section_penalty_score

        if verbose:
            print("St base: {:.2f}, St addl: {:.2f}, S conflict: {:.2f}, T conflict: {:.2f}, Per spread: {:.2f}, Sec penalty: {:.2f}".format(student_base_score,student_addl_score,student_conflict_score,teacher_conflict_score,period_spread_score,section_penalty_score))
            print(score,score+addl_score)

        return score if static else score+addl_score


    def set_progress(self):
        score=self.preliminary_score(static=1)
        global _CLOSENESS_TO_COMPLETION
        _CLOSENESS_TO_COMPLETION = max(0, (score + .01) / self.theoretical_max_score)
        self.initialize_weights()

    def score_student(self,student):
        st_conflict_score,addl_score=self.score_student_sections(student)
        base_score=st_conflict_score
        base_score+=self.score_student_courses(student)
        return (base_score+addl_score,base_score,st_conflict_score)

    def score_student_sections(self,student):
        base_score = 0
        periods_yr = set()
        periods_s1 = set()
        periods_s2 = set()
        addl_score = 0
        for j in student.sched:
            k = j.period
            if j.semester == 0:
                if k in periods_yr or k in periods_s1 or k in periods_s2:
                    base_score += self.student_conflict_score_delta
                periods_yr.add(k)
            elif j.semester == 1:
                if k in periods_yr or k in periods_s1:
                    base_score += self.student_conflict_score_delta
                periods_s1.add(k)
            elif j.semester == 2:
                if k in periods_yr or k in periods_s2:
                    base_score += self.student_conflict_score_delta
                periods_s2.add(k)
            addl_score += self.rare_class_bonus * len(self.course_sections[j.course]) ** -2.5
        return base_score,addl_score

    def score_student_courses(self,student):
        courses={}
        base_score=0
        for i in student.sched:
            if i.course not in courses:
                courses[i.course]=0
            courses[i.course]+=1
        for i,j in courses.items():
            if i in student.courses.courses:
                if j==1:
                    if i.duration=='year':
                        base_score += self.correct_yr_course_score_delta
                    else:
                        base_score += self.correct_sem_course_score_delta
                else:
                    base_score += self.duplicate_correct_course_score_delta
        return base_score


    def score(self):
        return self.preliminary_score()

    def weighted_score(self):
        return 1.05**self.score()

    def is_viable(self):
        return 1

    def remove_teacher_conflicts(self):
        outer_conflicts=-1
        while outer_conflicts!=0:
            outer_conflicts=0
            for i in self.teachers.values():
                n=0
                conflicts=-1
                while conflicts!=0:
                    n+=1
                    if n>100000:
                        # print(i.teacherID)
                        print('Teacher {} has unresolveable conflicts. Exiting operation.'.format(i.teacherID))
                        raise ValueError
                    conflicts=0
                    periods={}
                    for j in sorted(i.sched,key=lambda i:random.random()):
                        k = j.period
                        if k not in periods:
                            periods[k] = []
                        same_period = periods[k]
                        if k==0:
                            self.mutate_period(j,verbose=0)
                            conflicts+=1
                            outer_conflicts+=1
                        if j.semester == 0:
                            for m in same_period:
                                if m not in j.teamed2:
                                    self.mutate_period(j,verbose=0)
                                    conflicts+=1
                                    outer_conflicts += 1
                                    break
                            periods[k].append(j)
                        elif j.semester == 1:
                            for m in same_period:
                                if m not in j.teamed2:
                                    if m.semester == 1 or m.semester == 0:
                                        self.mutate_period(j,verbose=0)
                                        conflicts+=1
                                        outer_conflicts += 1
                                        break
                            periods[k].append(j)
                        elif j.semester == 2:
                            for m in same_period:
                                if m not in j.teamed2:
                                    if m.semester == 2 or m.semester == 0:
                                        self.mutate_period(j,verbose=0)
                                        conflicts+=1
                                        outer_conflicts += 1
                                        break
                            periods[k].append(j)
            conflicts=-1
            while conflicts!=0:
                conflicts=0
                for i in self.sections.values():
                    inner_conflicts=-1
                    n=0
                    while inner_conflicts!=0:
                        inner_conflicts=0
                        n+=1
                        if i.period not in i.allowed_periods:
                            conflicts += 1
                            inner_conflicts += 1
                            outer_conflicts += 1
                            self.mutate_period(i, verbose=0, allow_randomness=1)
                        if i.teamed1:
                            periods=[i.period]
                            for j in i.teamed1:
                                periods.append(j.period)
                            if len(set(periods))!=len(periods):
                                conflicts+=1
                                inner_conflicts+=1
                                outer_conflicts += 1
                                self.mutate_period(i,verbose=0,allow_randomness=1)
                                for k in i.teamed1:
                                    self.mutate_period(k,verbose=0,allow_randomness=1)
                        if n>100:
                            print(i.__repr__())



    def optimize_student(self,student,max_it=1000,skip_if_filled=0):
        for i in range(max_it):
            score,student_score,conflict_score=self.score_student(student)
            if skip_if_filled and student_score==self.num_periods*self.correct_course_score_delta:
                return
            courses={}
            old_sections = []
            courses_randomized=list(student.courses.courses)
            random.shuffle(courses_randomized)#sorted(student.courses.courses, key=lambda i: random.random())
            for _ in range(2):
                for j in courses_randomized:
                    courses[j]=[]
                    for k in student.sched:
                        if j==k.course:
                            courses[j].append(k)
                for i in courses_randomized:
                    if len(courses[i])==0:
                        break
                else:
                    i=courses_randomized[0]
                    sect=random.choice(courses[i])
                    sect.remove_student(student)
                    old_sections.append(sect)
                    continue
                break

            free_periods={}



            s=self.course_sections[i] if i in self.course_sections else []
            random.shuffle(s)
            allow_full_period=random.random()<.05
            for i in range(self.num_periods):
                free_periods[i+1]=[1,2]
            for i in student.sched:
                if i.semester==0:
                    free_periods[i.period]=[]
                else:
                    try:
                        free_periods[i.period].remove(i.semester)
                    except ValueError:
                        pass
            new_section=None
            if not allow_full_period:
                for i in s:
                    if i.space_available():
                        p=i.period
                        if i.semester==0:
                            if not (1 in free_periods[i.period] and 2 in free_periods[i.period]):
                                continue
                        elif i.semester not in free_periods[i.period]:
                            continue
                        new_section=i
                        break
            if new_section is None:
                for i in s:
                    if i.space_available():
                        new_section=i
                        break
                if new_section is None:
                    continue

            # for i in student.sched:
            #     if i.period==new_section.period:
            #         if {i.semester,new_section.semester}!={1,2}:
            #             old_sections.append(i)
            # for i in old_sections:
            #     try:
            #         i.remove_student(student)
            #     except ReferenceError:
            #         pass
            old_sections=new_section.add_student_removing_conflicts(student)
            new_score = self.score_student(student)[0]
            # raise NotImplementedError#Need to check that teamed things can be slotted in too.
            if new_score>=score or random.random()<2**(-8*(score-new_score)):
                # if score>new_score:
                #     print(score-new_score)
                pass
            else:
                new_section.remove_student(student)
                for i in old_sections:
                    i.add_student_basic(student)
        # print(score, self.score_student(student)[0])

    def copy(self):
        sched=master_schedule(self.num_periods, self.stock_classrooms, self.stock_courses, self.stock_teachers, self.stock_students, self.stock_sections)
        sched.fill_new(fill_sections=0)
        for i in self.sections.values():
            s=Section(i.id)
            sched.sections[s.id] = s
            for j in i.teachers:
                teacher = sched.teachers[j.teacherID]
                s.add_teacher(teacher)
            for j in i.students:
                student = sched.students[j.studentID]
                s.add_student_basic(student)
            for j in i.classrooms:
                classroom = sched.classrooms[j.num]
                s.add_classroom(classroom)

            course = self.stock_courses[i.course.courseID]
            s.set_course(course)
            s.set_semester(i.semester)
            s.set_max_students(i.maxstudents)
            s.set_period(i.period)
            s.set_allowed_periods(i.allowed_periods)
            if i.period_fixed:
                s.fix_period()
            for j in i.teamed1:
                sched.teams1.append((s, j.id))
            for j in i.teamed2:
                sched.teams2.append((s, j.id))
            for j in i.teamed3:
                sched.teams3.append((s, j.id))
        for i, j in sched.teams1:
            other = sched.sections[j]
            if other not in i.teamed1:
                i.team_1(other)
        for i, j in sched.teams2:
            other = sched.sections[j]
            if other not in i.teamed2:
                i.team_2(other)
        for i, j in sched.teams3:
            other = sched.sections[j]
            if other not in i.teamed3:
                i.team_3(other)
        for sect in sched.sections.values():
            course=sect.course
            if course not in sched.course_sections:
                sched.course_sections[course] = []
            sched.course_sections[course].append(sect)



        return sched

    def __str__(self):
        return '{} object, score={} ({})'.format(self.__class__.__name__,self.score(),self.preliminary_score(static=1))


class hill_climb_solo_2:
    def __init__(self, dataclass, num_periods,classrooms,courses,teachers,students,sections,outfolder, *args, **kwargs):
        self.dataclass = dataclass
        assert issubclass(self.dataclass, chromosome)
        self.current_sched = None
        self.outfolder=outfolder
        j = self.dataclass(num_periods,classrooms,courses,teachers,students,sections,*args, **kwargs)
        j.retrieve_schedule(outfolder)
        # if not j.is_viable():
        #     raise UnviableScheduleError
        self.current_sched=j
        # crss=[]
        # for i in j.stock_students.values():
        #     for k in i.courses.courses:
        #         if k not in j.course_sections and k not in crss:
        #             crss.append(k)
        # print(len(crss))
        # for i in crss:
        #     print(i)
        self.current_sched.initialize_weights()


    def solve(self, verbose=0, print_every=500):
        # global _NUM_ITERATIONS
        global _ITERATION
        # _NUM_ITERATIONS=num_iterations
        last_save=-1
        first_it=1
        while 1:
            self.current_sched.initialize_weights()
            if (time.perf_counter()-_START_TIME)//_SAVE_TIME>last_save:
                last_save=(time.perf_counter()-_START_TIME)//_SAVE_TIME
                save_schedule(self.current_sched, self.outfolder)
                print_schedule(self.current_sched, self.outfolder)
            _ITERATION+=1
            i=_ITERATION
            if first_it == 1:
                self.current_sched.remove_teacher_conflicts()
                self.current_sched.score()
                self.current_sched.initialize_weights()
            if first_it==1 or i<10 or i % print_every == 0:
                first_it=0
                print('Round {}: score {:.2f} ({:.2f}). Elapsed time: {}.'.format(i,self.current_sched.score(),self.current_sched.preliminary_score(static=1),current_time_formatted()))
            new_organism = self.current_sched.copy()
            new_organism.initialize_weights()
            if i%20==1:
                for _ in range(10):
                    for i in new_organism.students.values():
                        new_organism.optimize_student(i, max_it=10)
            else:
                num_mutations=int(1+random.random()*(1*(1-_CLOSENESS_TO_COMPLETION))) if i%20!=1 else 0
                for i in range(num_mutations):
                    new_organism.mutate_period()
                for _ in range(10):
                    for i in new_organism.students.values():
                        new_organism.optimize_student(i,max_it=1)
            print('New:')
            new_score=new_organism.preliminary_score(verbose=1)
            print('Old:')
            old_score=self.current_sched.preliminary_score(verbose=1)
            delta_score=old_score-new_score
            if new_score>=old_score or random.random()<(.5-.5*_CLOSENESS_TO_COMPLETION)**3:#10**(-5*_CLOSENESS_TO_COMPLETION)*
                self.current_sched=new_organism
            # print('',old_score,'\n',new_score)
            self.current_sched.set_progress()
            if _CLOSENESS_TO_COMPLETION>1:
                print('Scheduling complete.')
                break

            # if _ITERATION>420:
            #     break

def save_schedule(master_sched,outfolder,verbose=1):
    # return
    # print('Saving schedules not yet implemented.')
    # print('Saving progress. '+current_time_formatted(round=0))
    if verbose:
        print('Saving schedule. ({})'.format(_ITERATION))
    outfile=outfolder+'/schedule.db'
    connection = sqlite3.connect(outfile)
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS schedule ;')
    cursor.execute('CREATE TABLE schedule (section text,students text,period text);')
    command='INSERT INTO schedule(section,students,period) VALUES(?,?,?);'
    for i in master_sched.sections.values():
        cursor.execute(command,(i.id,'|'.join((j.studentID for j in i.students)),i.period))
    cursor.execute('UPDATE metadata SET iteration=?,time_elapsed=?',(_ITERATION,time.perf_counter()-_START_TIME))
    connection.commit()
    connection.close()
    # print('Finished saving progress. '+current_time_formatted(round=0))

def print_schedule(master_sched,outfolder):
    # master_sched = fill_in_schedule(master_sched)
    # print(master_sched)

    filename = outfolder+'/readable_schedule.txt'

    with open(filename, 'w') as f:
        f.write(str(len(master_sched.sections)) + '\n')
        for i in master_sched.sections.values():
            f.write(i.long_string())
            f.write('\n\n')
        f.write(str(len(master_sched.students)) + '\n')
        for i in master_sched.students.values():
            f.write(str(i))
            f.write(i.medium_string())
            f.write('\n\n')


def diagnostics(master_sched):
    #Teacher conflicts
    #Student conflicts
    #Student schedule fills (w/ see counselor)
    pass

def fill_in_schedule(sched,num_it=3):
    sections=sched.course_sections
    sched.initialize_weights()
    it=0
    m_it=num_it*len(sched.students)
    print('Beginning post-processing.')
    for i in range(num_it):
        for student in sched.students.values():
            it+=1
            if it%100==0:
                print('Post-processing item {} of {}'.format(it,m_it))
            sched.optimize_student(student,max_it=200,skip_if_filled=0)
    print('Elapsed time: {}.'.format(current_time_formatted()))
    return sched
#remove duplicated periods

def post_process(sched):
    #assign homerooms
    #distribute IBET, HUM, sem/global, CHUM, GHUM
    #8th online period?
    # add See Counselor
    return sched

def current_time_formatted(round=1):
    t=time.perf_counter()-_START_TIME
    hr=int(t//3600)
    min=int(t//60)%60
    sec=t%60
    if round:
        if hr>0:
            return '{} hr, {} min, {:.2f} sec'.format(hr,min,sec)
        elif min>0:
            return '{} min, {:.2f} sec'.format(min,sec)
        else:
            return '{:.2f} sec'.format(sec)
    else:
        return str(t)

if __name__=='__main__':
    pass
    # # for i in range(100):
    # #     master_schedule().fill_new()
    # solver=genetic_solver(knapsack,population_size=10)
    # winner=solver.solve(num_iterations=10000, verbose=1)
    # #     # print(winner)

