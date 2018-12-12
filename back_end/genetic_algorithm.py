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

class knapsack(chromosome):
    def __init__(self,*args,**kwargs):
        super(knapsack,self).__init__(*args,**kwargs)
        self.items = [(10, 10), (6, 5), (7, 8), (2, 1), (3,3), (7,2),(9,1),(0, 0)]
        self.capacity = 20
        self.num_items=4
        self.score_var=None
        self.weighted_score_var=None
        self.recompute_score=1

    def blank_new(self):
        self.l=[None for i in range(self.num_items)]
        self.recompute_score=1

    def randomize_new(self):
        self.l=[]
        for i in range(self.num_items):
            self.l.append(random.choice(self.items))
        self.recompute_score=1

    def mutate(self):
        index=random.randint(0, self.num_items - 1)
        self.l[index]=random.choice(self.items)
        self.recompute_score=1

    def score(self):
        if self.score_var is None or self.recompute_score:
            if sum((i[0] for i in self.l))>self.capacity:
                self.score_var=-1
            else:
                self.score_var=sum((i[1] for i in self.l))
        return self.score_var

    def weighted_score(self):
        if self.weighted_score_var is None:
            self.weighted_score_var=1.2**self.score()
        return self.weighted_score_var

    def is_viable(self):
        return self.score()>=0

    @staticmethod
    def breed(a,b):
        child=knapsack()
        child.blank_new()
        # min_a,max_a=sorted([random.randint(0,a.num_items),random.randint(0,a.num_items)])
        for i in range(a.num_items):
            if random.getrandbits(1):
                child.l[i]=a.l[i]
            else:
                child.l[i]=b.l[i]
        if random.random()<.2:
            child.mutate()
        return child

    def __str__(self):
        return '{}, score={}'.format(self.l,self.score())

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
        self.teams=[]
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
                    s.add_student(student)
                for j in i.classrooms:
                    classroom=self.classrooms[j.num]
                    s.add_classroom(classroom)
                for j in i.courses:
                    course=self.stock_courses[j.courseID]
                    s.add_course(course)
                s.set_semester(i.semester)
                s.set_max_students(i.maxstudents)
                s.set_period(i.period)
                if i.period_fixed:
                    s.fix_period()
                for j in i.teamed_sections:
                    self.teams.append((s,j.id))
            for sect in self.sections.values():
                for course in sect.courses:
                    if course not in self.course_sections:
                        self.course_sections[course] = []
                    self.course_sections[course].append(sect)
            for i,j in self.teams:
                other=self.sections[j]
                i.team_with(other)

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
                        s.add_student(self.students[i])
        else:
            pass#do nothing
        #DON'T COMMIT
        connection.close()

    def randomize_new(self):
        self.fill_new()


    def mutate_period(self):
        mutating_section = random.choice(tuple(self.sections.values()))
        p = random.choice(mutating_section.allowed_periods)
        try:
            self.change_to_period(mutating_section, p, [])
        except InvalidPeriodError:
            pass

    def change_to_period(self, section, new_period, reached):
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
                    if j.period==new_period:
                        self.change_to_period(j,old_period,reached)
            for j in section.teamed_sections:
                if j.period == new_period:
                    self.change_to_period(j, old_period, reached)
        except InvalidPeriodError:
            section.set_period(old_period)
            raise

    def initialize_weights(self):
        self.student_conflict_score_delta = -200
        self.teacher_conflict_score_delta = -250
        self.correct_course_score_delta = 4
        self.theoretical_max_score = self.correct_course_score_delta * len(self.stock_students) * self.num_periods

        self.duplicate_correct_course_score_delta = -5
        self.rare_class_bonus = 8 * (1 - _CLOSENESS_TO_COMPLETION**2)
        self.section_in_prohibited_period_delta=-1000
        self.course_period_overlap=-10

    def preliminary_score(self,static=0):
        if not self.initialized:
            raise ReferenceError
        score=0
        addl_score=0

        self.initialize_weights()

        for i in self.students.values():
            student_score,_=self.score_student(i)
            score+=_
            addl_score+=student_score-_

        for i in self.teachers.values():
            periods_yr = set()
            periods_s1 = set()
            periods_s2 = set()
            for j in i.sched:
                k = j.period
                if j.semester == 0:
                    if k in periods_yr or k in periods_s1 or k in periods_s2:
                        score += self.teacher_conflict_score_delta
                    periods_yr.add(k)
                elif j.semester == 1:
                    if k in periods_yr or k in periods_s1:
                        score += self.teacher_conflict_score_delta
                    periods_s1.add(k)
                elif j.semester == 2:
                    if k in periods_yr or k in periods_s2:
                        score += self.teacher_conflict_score_delta
                    periods_s2.add(k)

        for i in self.course_sections.values():
            period_counts={}
            for j in i:
                if j.period not in period_counts:
                    period_counts[j.period]=0
                period_counts[j.period]+=1
            for j in period_counts.values():
                if j>1:
                    addl_score+=j**2*self.course_period_overlap

        for i in self.sections.values():
            if i.period not in i.allowed_periods:
                score+=self.section_in_prohibited_period_delta

        for i in self.sections.values():
            if len(i.students)>i.maxstudents:
                score-=100

        return score if static else score+addl_score


    def set_progress(self):
        score=self.preliminary_score(static=1)
        global _CLOSENESS_TO_COMPLETION
        _CLOSENESS_TO_COMPLETION = max(0, (score + .01) / self.theoretical_max_score)
        self.initialize_weights

    def score_student(self,student):
        base_score,addl_score=self.score_student_sections(student)
        base_score+=self.score_student_courses(student)
        return (base_score+addl_score,base_score)

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
            addl_score += self.rare_class_bonus * len(self.course_sections[next(iter(j.courses))]) ** -2.5
        return base_score,addl_score

    def score_student_courses(self,student):
        courses={}
        base_score=0
        for i in student.sched:
            for j in i.courses:
                if j not in courses:
                    courses[j]=0
                courses[j]+=1
        for i,j in courses.items():
            if i in student.courses.courses:
                if j==1:
                    base_score += self.correct_course_score_delta
                else:
                    base_score += self.duplicate_correct_course_score_delta
        return base_score


    def score(self):
        return self.preliminary_score()

    def weighted_score(self):
        return 1.05**self.score()

    def is_viable(self):
        return 1

    def optimize_student(self,student,max_it=1000,skip_if_filled=0):
        for i in range(max_it):
            score,student_score=self.score_student(student)
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
                        if j in k.courses:
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

            s=sorted(self.course_sections[i],key=lambda i:random.random())
            new_section=None
            for i in s:
                if i.space_available():
                    new_section=i
                    break
            if new_section is None:
                continue

            for i in student.sched:
                if i.period==new_section.period:
                    old_sections.append(i)
            for i in old_sections:
                try:
                    i.remove_student(student)
                except ReferenceError:
                    pass
            new_section.add_student(student)
            new_score = self.score_student(student)[0]
            if new_score<score:
                new_section.remove_student(student)
                for i in old_sections:
                    i.add_student(student)


    @staticmethod
    def breed(a,b):
        sched=master_schedule()
        sched.fill_new(fill_sections=0)
        for i in a.sections.values():
            if random.getrandbits(1):
                s=a.sections[i.id]
            else:
                s=b.sections[i.id]
            s=Section(s.id)
            sched.sections[s.id] = s
            for j in i.teachers:
                teacher = sched.teachers[j.teacherID]
                s.add_teacher(teacher)
            for j in i.students:
                student = sched.students[j.studentID]
                s.add_student(student)
            for j in i.classrooms:
                classroom = sched.classrooms[j.num]
                s.add_classroom(classroom)
            for j in i.courses:
                course = self.stock_courses[j.courseID]
                s.add_course(course)
            s.set_semester(i.semester)
            s.set_max_students(i.maxstudents)
            s.set_period(i.period)
            if i.period_fixed:
                s.fix_period()
            for j in i.teamed_sections:
                sched.teams.append((s, j.id))
        for i,j in sched.teams:
            other=sched.sections[j]
            i.team_with(other)
        for sect in sched.sections.values():
            for course in sect.courses:
                if course not in sched.course_sections:
                    sched.course_sections[course] = []
                sched.course_sections[course].append(sect)
        return sched


    # def copy(self):
    #     return master_schedule.breed(self,self)

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
                s.add_student(student)
            for j in i.classrooms:
                classroom = sched.classrooms[j.num]
                s.add_classroom(classroom)
            for j in i.courses:
                course = self.stock_courses[j.courseID]
                s.add_course(course)
            s.set_semester(i.semester)
            s.set_max_students(i.maxstudents)
            s.set_period(i.period)
            if i.period_fixed:
                s.fix_period()
            for j in i.teamed_sections:
                sched.teams.append((s, j.id))
        for i,j in sched.teams:
            other=sched.sections[j]
            i.team_with(other)
        for sect in sched.sections.values():
            for course in sect.courses:
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
        if not j.is_viable():
            raise UnviableScheduleError
        self.current_sched=j


    def solve(self, verbose=0, print_every=500):
        # global _NUM_ITERATIONS
        global _ITERATION
        # _NUM_ITERATIONS=num_iterations
        last_save=-1
        first_it=1
        while 1:
            if (time.perf_counter()-_START_TIME)//_SAVE_TIME>last_save:
                last_save=(time.perf_counter()-_START_TIME)//_SAVE_TIME
                save_schedule(self.current_sched, self.outfolder)
                print_schedule(self.current_sched, self.outfolder)
            _ITERATION+=1
            i=_ITERATION
            if first_it==1 or i<10 or i % print_every == 0:
                first_it=0
                print('Round {}: score {:.2f} ({}). Elapsed time: {}.'.format(i,self.current_sched.score(),self.current_sched.preliminary_score(static=1),current_time_formatted()))
            new_organism = self.current_sched.copy()
            num_mutations=int(1+random.random()*(3+15*(1-_CLOSENESS_TO_COMPLETION)))
            for i in range(num_mutations):
                new_organism.mutate_period()
            new_organism.initialize_weights()
            for _ in range(2):
                for i in new_organism.students.values():
                    new_organism.optimize_student(i,max_it=15)
            new_score=new_organism.preliminary_score()
            old_score=self.current_sched.preliminary_score()
            if new_score>=old_score:
                self.current_sched=new_organism
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

