from basics import *
import random
# import numpy as np
import time
# VERBOSE=1
_NUM_ITERATIONS=None
_ITERATION=None
_START_TIME=time.perf_counter()

class NotImplemented(Exception):
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
        return f'{self.__class__.__name__} object, score={self.score()}'

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
        return f'{self.l}, score={self.score()}'

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

# class genetic_solver:
#     def __init__(self,dataclass,population_size=100,*args,**kwargs):
#         self.dataclass=dataclass
#         assert issubclass(self.dataclass,chromosome)
#         self.population=[]
#         self.num_organisms=population_size
#         # self.population=np.empty(self.num_organisms)
#         for i in range(self.num_organisms):
#             j=self.dataclass(*args,**kwargs)
#             j.randomize_new()
#             while not j.is_viable():
#                 j.randomize_new()
#             self.population.append(j)
#
#
#
#     def prune_population(self):
#         # print('PRUNING POPULATION')
#         self.population.sort(key=lambda i:-i.weighted_score())
#         self.population=self.population[:self.num_organisms]
#
#
#     def solve(self, num_iterations=0, verbose=0,print_every=500):
#         global _NUM_ITERATIONS
#         global _ITERATION
#         _NUM_ITERATIONS=num_iterations
#         self.population = [i for i in self.population if i.is_viable()]
#         for i in range(num_iterations):
#             _ITERATION=i
#             if verbose:
#                 print(f'---------Round {i}---------')
#                 print([i.score() for i in self.population])
#                 print(f'Max score: {max([i.score() for i in self.population])}')
#             else:
#                 if i%print_every==0:
#                     print(f'Round {i}: max {max([i.score() for i in self.population])}')
#             if len(self.population)<2:
#                 print('No viable population to breed. Exiting operation.')
#                 return
#             if len(self.population)>10*self.num_organisms:
#                 self.prune_population()
#
#             weights=np.array([o.weighted_score() for o in self.population])
#             weights/=sum(weights)
#
#             a,b=weighted_choice(self.population,2,weights)
#             for i in range(5):
#                 new_organism=self.dataclass.breed(a,b)
#                 # if verbose:
#                 #     print(f'Breed {a} and {b}; result is {new_organism}')
#                 if new_organism.is_viable:
#                     self.population.append(new_organism)
#                 org2=new_organism.copy()
#                 org2.mutate()
#                 if org2.is_viable:
#                     self.population.append(org2)
#         winner=max(self.population,key=lambda i:i.score())
#         if verbose:
#             print(f'Winner: {winner}')
#         return winner

class master_schedule(chromosome):
    #criteria, data structures
    def __init__(self,*args,**kwargs):
        super(master_schedule, self).__init__(*args, **kwargs)
        self.num_periods=School.num_periods
        self.sections={}
        self.initialized = 0
        self.course_sections = {}


    def blank_new(self):
        pass

    def fill_new(self,fill_sections=1):
        self.teachers={}
        self.students={}
        self.classrooms={}
        for i in School.teachers.values():
            self.teachers[i.teacherID]=i.copy()
        for i in School.students.values():
            self.students[i.studentID]=i.copy()
        for i in School.classrooms.values():
            self.classrooms[i.num]=Classroom(i.num)
        self.teams=[]
        self.initialized=1
        if fill_sections:
            for i in School.sections.values():
                s=Section(i.id,keep_record=0)
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
                    course=School.courses[j.courseID]
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


    def randomize_new(self):
        self.fill_new()

    def mutate(self):
        # if random.random()<.5:
        #     return
        # for _ in range(random.randint(1,5)):

        # if random.random()<.9:
        #     continue
        if (random.random()<(1-.9*(_ITERATION/_NUM_ITERATIONS)) or mutating_section.maxstudents==0) and not mutating_section.period_fixed:
            self.mutate_period()
            return

        mutating_section = random.choice(tuple(self.sections.values()))
        if random.random()<.5 and mutating_section.students:
            student=random.choice(tuple(mutating_section.students))
            mutating_section.remove_student(student)
            courses=[]
            for requested_course in student.courses.courses:
                for section_taking in student.sched:
                    if requested_course in section_taking.courses:
                        break
                else:
                    courses.append(requested_course)
            occupied_periods=set()
            for i in student.sched:
                occupied_periods.add(i.period)
            for course_to_add in courses:
                for section_of_course in self.course_sections[course_to_add]:
                    if section_of_course.period not in occupied_periods and section_of_course.space_available():
                        section_of_course.add_student(student)
                        return
            # for j in self.sections.values():
            #     if len(j.students)>j.maxstudents:
            #         continue
            #     for n in j.courses:
            #         if n in student.courses.courses:
            #             for m in student.sched:
            #                 if n in m.courses:
            #                     break
            #             else:
            #                 for m in student.sched:
            #                     if j.period==m.period and not {m.semester,j.semester}=={1,2}:
            #                         break
            #                 else:
            #                     j.add_student(student)
            #                     break
            #     else:
            #         continue
            #     break


        else:
            for j in range(30):
                student = random.choice(tuple(self.students.values()))
                if any([j in student.courses.courses for j in mutating_section.courses]):
                    l=[j for j in mutating_section.courses if j in student.courses.courses]
                    for m in l:
                        for j in student.sched:
                            if m in j.courses:
                                continue
                    break
            else:
                return
            if student not in mutating_section.students and len(mutating_section.students)<mutating_section.maxstudents:
                mutating_section.add_student(student)

    def mutate_period(self):
        mutating_section = random.choice(tuple(self.sections.values()))
        p = random.choice(mutating_section.allowed_periods)
        self.change_to_period(mutating_section, p, [])

    def change_to_period(self, section, new_period, reached):
        if new_period==section.period or section in reached:
            return
        reached.append(section)
        old_period=section.period
        section.set_period(new_period)
        for i in section.teachers:
            for j in i.sched:
                if j.period==new_period:
                    self.change_to_period(j,old_period,reached)

    def initialize_weights(self):
        self.student_conflict_score_delta = -200 #* (_ITERATION / _NUM_ITERATIONS + .1) ** 2.2
        self.teacher_conflict_score_delta = -250  # *(_ITERATION/_NUM_ITERATIONS+.1)
        # missing_score_delta=-1#*(_ITERATION/_NUM_ITERATIONS)**2
        self.correct_course_score_delta = 4
        self.duplicate_correct_course_score_delta = -5
        self.rare_class_bonus = 8 * (1 - (_ITERATION / _NUM_ITERATIONS))
        self.missing_teamed_class_delta=-2
        self.section_in_prohibited_period_delta=-1000
        self.course_period_overlap=-1

    def preliminary_score(self,static=0):
        if not self.initialized:
            raise ReferenceError
        score=0

        self.initialize_weights()

        for i in self.students.values():
            student_score,_=self.score_student(i)
            score+=(student_score if not static else _)

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
                    score+=j**2*self.course_period_overlap if not static else 0

        for i in self.sections.values():
            if i.period not in i.allowed_periods:
                score+=self.section_in_prohibited_period_delta

        for i in self.sections.values():
            if len(i.students)>i.maxstudents:
                score-=100
        return score


    def score_student(self,student):
        base_score,addl_score=self.score_student_sections(student)
        base_score+=self.score_student_courses(student)


        # for j in student.courses.courses:
        #     times_represented = 0
        #     for k in student.sched:
        #         if j in k.courses:
        #             times_represented += 1
        #     if times_represented == 1:
        #         base_score += self.correct_course_score_delta
        #     elif times_represented > 1:
        #         base_score += self.duplicate_correct_course_score_delta

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
            for i in j.teamed_sections:
                if i not in j.sched:
                    base_score += self.missing_teamed_class_delta
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
            for i in s:
                if i.space_available():
                    new_section=i
                    break
            # else:
            #     continue


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
            s=Section(s.id,keep_record=0)
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
                course = School.courses[j.courseID]
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


    def copy(self):
        return master_schedule.breed(self,self)

    def __str__(self):
        return f'{self.__class__.__name__} object, score={self.score()} ({self.preliminary_score(static=1)})'

# class hill_climb:
#     def __init__(self, dataclass, population_size=100, *args, **kwargs):
#         self.dataclass = dataclass
#         assert issubclass(self.dataclass, chromosome)
#         self.population = []
#         self.num_organisms = population_size
#         # self.population=np.empty(self.num_organisms)
#         for i in range(self.num_organisms):
#             j = self.dataclass(*args, **kwargs)
#             j.randomize_new()
#             while not j.is_viable():
#                 j.randomize_new()
#             self.population.append(j)
#
#     def prune_population(self):
#         # print('PRUNING POPULATION')
#         self.population.sort(key=lambda i: -i.weighted_score())
#         self.population = self.population[:self.num_organisms]
#
#     def solve(self, num_iterations=0, verbose=0, print_every=500,):
#         global _NUM_ITERATIONS
#         global _ITERATION
#         _NUM_ITERATIONS=num_iterations
#         self.population = [i for i in self.population if i.is_viable()]
#         for i in range(1,num_iterations+1):
#             if i%200==0:
#                 print(i)
#             _ITERATION=i+1
#             if verbose:
#                 print(f'---------Round {i}---------')
#                 print([i.score() for i in self.population])
#                 print(f'Max score: {max([i.score() for i in self.population])}')
#             else:
#                 if i % print_every == 0:
#                     print(f'Round {i}: max {max([i.score() for i in self.population])}')
#             # if len(self.population) < 1:
#             #     print('No viable population to breed. Exiting operation.')
#             #     return
#             if len(self.population) > 2 * self.num_organisms:
#                 self.prune_population()
#
#             weights = np.array([o.weighted_score() for o in self.population])
#             weights /= sum(weights)
#
#             # l = weighted_choice(self.population, 2, weights)
#             l=[]
#
#             for a in self.population:
#                 l.append(a)
#                 new_organism = a.copy()
#                 new_organism.mutate()
#                 if new_organism.is_viable:
#                     l.append(new_organism)
#                 # a=new_organism
#             self.population=l
#
#         winner = max(self.population, key=lambda i: i.score())
#         if verbose:
#             print(f'Winner: {winner}')
#         return winner
#
# class hill_climb_solo:
#     def __init__(self, dataclass, population_size=100, *args, **kwargs):
#         self.dataclass = dataclass
#         assert issubclass(self.dataclass, chromosome)
#         self.population = None
#         self.num_organisms = population_size
#         # self.population=np.empty(self.num_organisms)
#         for i in range(self.num_organisms):
#             j = self.dataclass(*args, **kwargs)
#             j.randomize_new()
#             while not j.is_viable():
#                 j.randomize_new()
#             self.population=j
#
#     def prune_population(self):
#         # print('PRUNING POPULATION')
#         self.population.sort(key=lambda i: -i.weighted_score())
#         self.population = self.population[:self.num_organisms]
#
#     def solve(self, num_iterations=0, verbose=0, print_every=500,):
#         global _NUM_ITERATIONS
#         global _ITERATION
#         _NUM_ITERATIONS=num_iterations
#         # self.population = [i for i in self.population if i.is_viable()]
#         for i in range(1,num_iterations+1):
#             if i%200==0:
#                 print(i)
#             _ITERATION=i
#             # if verbose:
#             #     print(f'---------Round {i}---------')
#             #     print([i.score() for i in self.population])
#             #     print(f'Max score: {max([i.score() for i in self.population])}')
#             # else:
#             if i % print_every == 0:
#                 print(f'Round {i}: score {self.population.preliminary_score()}')
#             # if len(self.population) < 1:
#             #     print('No viable population to breed. Exiting operation.')
#             #     return
#             # if len(self.population) > 2 * self.num_organisms:
#             #     self.prune_population()
#
#             # weights = np.array([o.weighted_score() for o in self.population])
#             # weights /= sum(weights)
#
#             # l = weighted_choice(self.population, 2, weights)
#             # l=[]
#
#             # for a in self.population:
#             new_organism = self.population.copy()
#             # if num_iterations*2/3<=i<=num_iterations*2/3+1:
#             #     new_organism=fill_in_schedule(new_organism)
#             # else:
#             new_organism.mutate()
#             # if new_organism.is_viable:
#                 # l.append(new_organism)
#             new_score=new_organism.preliminary_score()
#             old_score=self.population.preliminary_score()
#             if new_score>=old_score:
#                 self.population=new_organism
#                 # a=new_organism
#             # self.population=l
#
#         # winner = max(self.population, key=lambda i: i.score())
#         winner=self.population
#         if verbose:
#             print(f'Winner: {winner}')
#         return winner

class hill_climb_solo_2:
    def __init__(self, dataclass, population_size=1, *args, **kwargs):
        self.dataclass = dataclass
        assert issubclass(self.dataclass, chromosome)
        self.population = None
        self.num_organisms = population_size
        for i in range(self.num_organisms):
            j = self.dataclass(*args, **kwargs)
            j.randomize_new()
            while not j.is_viable():
                j.randomize_new()
            self.population=j


    def solve(self, num_iterations=0, verbose=0, print_every=500,):
        global _NUM_ITERATIONS
        global _ITERATION
        _NUM_ITERATIONS=num_iterations
        for i in range(1,num_iterations+1):
            # if i%200==0:
            #     print(i)
            _ITERATION=i
            if i<10 or i % print_every == 0:
                print(f'Round {i}: score {self.population.score():.2f} ({self.population.preliminary_score(static=1)}). Elapsed time: {current_time_formatted()}.')
            new_organism = self.population.copy()
            for i in range(int(1+5*random.random()*(1-_ITERATION/_NUM_ITERATIONS))):
                new_organism.mutate_period()
            new_organism.initialize_weights()
            for _ in range(2):
                for i in new_organism.students.values():
                    new_organism.optimize_student(i,max_it=15)
            new_score=new_organism.preliminary_score()
            old_score=self.population.preliminary_score()
            if new_score>=old_score:
                self.population=new_organism
        winner=self.population
        if verbose:
            print(f'Winner: {winner}')
        return winner

def diagnostics(master_sched):
    #Teacher conflicts
    #Student conflicts
    #Student schedule fills
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
                print(f'Post-processing item {it} of {m_it}')
            sched.optimize_student(student,max_it=200,skip_if_filled=0)
    print(f'Elapsed time: {current_time_formatted()}.')
    return sched
#remove duplicated periods

def post_process(sched):
    #assign homerooms
    #distribute IBET, HUM, sem/global, CHUM, GHUM
    #8th online period?
    # add See Counselor
    return sched

def current_time_formatted():
    t=time.perf_counter()-_START_TIME
    min=int(t//60)
    sec=t%60
    if min>0:
        return f'{min} min, {sec:.2f} sec'
    else:
        return f'{sec:.2f} sec'

if __name__=='__main__':
    pass
    # # for i in range(100):
    # #     master_schedule().fill_new()
    # solver=genetic_solver(knapsack,population_size=10)
    # winner=solver.solve(num_iterations=10000, verbose=1)
    # #     # print(winner)

