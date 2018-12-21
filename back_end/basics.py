"""
List of problems that need to be addressed:
- How does code deal with graduation requirements?
    - Is there a class for requirements?
    - Does every student object have a list of fulfilled and outstanding requirements?
    - Should type of class be a field in Course?
    - Should Course store the graduation requirements it fulfills?
    - Proposal for structure of graduation requirements: An list of requirements containing a mix of individual courses
      and lists of courses. An individual course is required for graduation, and one course in a list of courses is
      required as well.
        - Must deal with semester classes. This system doesn't handle them well or at all because it requires ways to
          define
"""
import random
import sys
import logging
import os
import time
# Global vars:
_course_creation_disabled= 1
# End global vars

def start_logging(save):
    logging.basicConfig(filename=save+'/log.log',level=logging.DEBUG, format="%(asctime)s|%(levelname)s|{}|%(message)s".format(os.getpid()))
    logging.Formatter.converter = time.gmtime

    class Logger(object):
        # Takes the place of stdout so everything printed to the console, in addition to being printed, also automatically gets logged.

        def __init__(self):
            self.terminal = sys.stdout
            self.dir=save

        def write(self, message):
            self.terminal.write(message)
            msg = message.strip()
            if msg:
                logging.info(msg)

        def flush(self):
            self.terminal.flush()


    class Err_Logger(object):
        # Takes the place of stdout so errors, in addition to being printed, also automatically get logged.

        def __init__(self):
            self.terminal = sys.stderr
            self.dir = save

        def write(self, message):
            self.terminal.write(message)
            msg = message.strip()
            if msg:
                logging.error(msg)

        def flush(self):
            self.terminal.flush()


    sys.stdout = Logger()
    sys.stderr = Err_Logger()
    global _SAVE
    _SAVE=save

def get_save_loc():
    return _SAVE

def set_global_num_periods(num_perds):
    global num_periods
    num_periods=num_perds

class Teacher:
    def __init__(self, myLastName, myFirstName, teacherID, willTeach):
        # willTeach is a dictionary that stores the courses that a teacher will teach. It stores the course
        # and associates it with the number of sections of that course the teacher is teaching.
        self.willTeach = willTeach#teacherCourses object

        # atSchool is a list of the periods during which a teacher is at school.
        # self.periods_available = periods_available#{int(i.strip()) for i in periods_available.split(';')}

        # firstName is a string that stores a teacher's first name
        self.firstName = myFirstName

        # lastName is a string that stores a teacher's last name
        self.lastName = myLastName
        self.teacherID=teacherID

        # leader is a boolean that holds True if the teacher holds a leadership position, and False if
        # the teacher does not.
        # self.leader = lead

        # sched is a variable that holds a dict of seven sections (some of which may be empty or planning sections).
        # sched is a dict so that classes can be accurately associated wither period numbers.
        # sched stores period number:section.
        # NOTE TO SELF: Consider automatically filling blocks when teacher won't be here with empty courses.
        self.sched = set()
        # if keep_record:
        #     global _all_teachers
        #     _all_teachers[self.teacherID]=self

    def long_string(self):
        # courses=self.willTeach.to_str() if self.willTeach else '\n\tNone'
        schedule='\n\n'.join([i.long_string() for i in self.sched]) if self.sched else '\n\tNot yet assigned.'
        return '{} {} ({})\n\tSchedule:\n{}'.format(self.firstName,self.lastName,self.teacherID,schedule)

    def copy(self):
        return Teacher(self.lastName,self.firstName,self.teacherID, self.willTeach)

    def __str__(self):
        return '{} {} ({})'.format(self.firstName,self.lastName,self.teacherID)

    def __hash__(self):
        return hash(self.teacherID)

    def __eq__(self,other):
        return isinstance(other, Teacher) and self.teacherID==other.teacherID


class Classroom:
    def __init__(self,roomNum):
        # num is a string that stores the classroom number
        self.num = roomNum

        # sched is a variable that holds an array of seven Sections (some of which may be empty or planning sections)
        self.sched = set()

    @staticmethod
    def classroom(roomNum):
        return Classroom(roomNum)

    def __str__(self):
        return 'Room {}'.format(self.num)

    def __hash__(self):
        return hash(object.__repr__(self))

class Course:
    def __init__(self, myName, shortName, myID, duration):
        if _course_creation_disabled:
            raise ValueError("Use Course.course to find an existing course or Course.create_new to create a new course.")
        # name is a string that stores the name of a course
        self.name = myName

        self.shortname=shortName

        # courseID is string that stores the ID of a course if one exists.
        self.courseID = myID

        self.duration=duration
        # self.max_students=max_students
        # Here, sched is simply an array of the sections when this course is taught. It will hold as many elements
        # as needed to list all of the sections of this course that are taught.
        # self.sched = set()

    # @staticmethod
    # def course(myID):
    #     if myID not in _courses:
    #         raise ReferenceError
    #         # courses[myID]=Course(myName, shortName, myID)
    #     return _courses[myID]

    @staticmethod
    def create_new(myName, shortName, myID, duration):
        global _course_creation_disabled
        _course_creation_disabled=0
        course=Course(myName, shortName, myID, duration)
        _course_creation_disabled = 1
        return course

    def __str__(self):
        return '{} {}'.format(self.courseID,self.name)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.courseID)

class Student:
    def __init__(self,myLastName, myFirstName,myID,myCourses):

        # studentID is a string that stores a student's student ID.
        self.studentID = myID

        self.firstName = myFirstName

        self.lastName = myLastName

        self.courses=myCourses#Student_Courses object

        self.teamed={}

        self.sched = set()

    # def add_section(self,section):
    #     if section in self.sched:
    #         return
    #     self.sched.add(section)
    #     section.students.add(self)
    #     for i in section.courses:
    #         if i in self.teamed:
    #             for j in self.teamed[i]:
    #                  section.add_student(j)
    #
    # def remove_section(self,section):
    #     if section not in self.sched:
    #         return
    #     self.sched.remove(section)
    #     section.students.remove(self)
    #     for i in section.courses:
    #         if i in self.teamed:
    #             for j in self.teamed[i]:
    #                 section.remove_student(j)

    def team(self,course,student):
        if course not in self.teamed:
            self.teamed[course]=[]
        self.teamed[course].append(student)
        if course not in student.teamed:
            student.teamed[course]=[]
        student.teamed[course].append(self)

    def long_string(self):
        requests=self.courses.to_str() if self.courses else '\n\t\tNone'
        schedule='\n\t'.join(self.sched) if self.sched else '\n\t\tNot yet assigned.'
        return '{} {} ({})\nRequests:\n{}\nSchedule:{}'.format(self.firstName,self.lastName,self.studentID,requests,schedule)

    def medium_string(self):
        requests = self.courses.to_str() if self.courses else '\n\t\tNone'
        sched='\n\t\t'.join([i.__repr__() for i in self.sched])
        return '{}\n\tSchedule:\n\t\t{}'.format(requests,sched)

    def __str__(self):
        return '{} {} ({})'.format(self.firstName,self.lastName,self.studentID)


    def copy(self):
        return Student(self.lastName,self.firstName,self.studentID,self.courses)

    def __hash__(self):
        return hash(self.studentID)

    def __eq__(self,other):
        return isinstance(other,Student) and self.studentID==other.studentID

class Section:
    def __init__(self, id):
        self.id=id
        self.teachers = set()
        self.students=set()
        self.courses=list()
        self.classrooms=set()
        self.period=1#random.randint(1,_num_periods)
        self.semester=None#0 is full year, 1 is S1, 2 is S2
        self.period_fixed=0
        self.teamed_sections=set()
        self.maxstudents=0
        self.minstudents=10
        self.allowed_periods=list(range(1,num_periods+1))

    def add_teacher(self,teacher):
        if teacher not in self.teachers:
            self.teachers.add(teacher)
        teacher.sched.add(self)

    def remove_teacher(self,teacher):
        if teacher not in self.teachers:
            raise ReferenceError
        self.teachers.remove(teacher)
        teacher.sched.remove(self)

    def add_student(self, student):
        # self.add_student_old(student)
        if student in self.students:
            return
        student.sched.add(self)
        self.students.add(student)
        for i in self.courses:
            if i in student.teamed:
                for j in student.teamed[i]:
                    self.add_student(j)
        for i in self.teamed_sections:
            i.add_student(student)

    def remove_student(self, student):
        # self.remove_student_old(student)
        if student not in self.students:
            return
        student.sched.remove(self)
        self.students.remove(student)
        for i in self.courses:
            if i in student.teamed:
                for j in student.teamed[i]:
                    self.remove_student(j)
        for i in self.teamed_sections:
            i.remove_student(student)


    # def add_student_old(self, student):
    #     if student in self.students:
    #         return
    #     self.students.add(student)
    #     student.sched.add(self)
    #     for i in self.teamed_sections:
    #         i.add_student(student)
    #
    # def remove_student_old(self, student):
    #     if student not in self.students:
    #         return#no error because teaming might direct us back here
    #     self.students.remove(student)
    #     student.sched.remove(self)
    #     for i in self.teamed_sections:
    #         i.remove_student(student)

    def add_classroom(self, room):
        if room not in self.classrooms:
            self.classrooms.add(room)
        room.sched.add(self)

    def remove_classroom(self, room):
        if room not in self.classrooms:
            raise ReferenceError
        self.classrooms.remove(room)
        room.sched.remove(self)

    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
        # course.sched.add(self)

    def remove_course(self, course):
        if course not in self.courses:
            raise ReferenceError
        self.courses.remove(course)
        # course.sched.remove(self)

    def fix_period(self):
        self.period_fixed=1

    def set_period(self,period,override=0):
        if not self.period_fixed or override:
            self.period=period
        else:
            raise AttributeError

    def set_semester(self,sem):
        self.semester=sem

    def team_with(self,other):
        self.teamed_sections.add(other)
        other.teamed_sections.add(self)

    def set_max_students(self,num):
        self.maxstudents=num
        if num==0:
            self.minstudents=0

    def set_min_students(self,num):
        self.minstudents=num

    def set_allowed_periods(self,allowed_periods):
        self.allowed_periods=allowed_periods
        self.period=self.allowed_periods[0]

    def space_available(self):
        return len(self.students)<=self.maxstudents-1

    def long_string(self):
        courses=", ".join([str(i) for i in self.courses])
        teachers = ", ".join([str(i) for i in self.teachers])
        rooms = ", ".join([str(i) for i in self.classrooms])
        allowed_pers = ' '+",".join([str(i) for i in self.allowed_periods])
        students = ", ".join([str(i) for i in self.students])
        # periods=", ".join([str(i) for i in self.period])
        teamedwith=', '.join([str(i) for i in self.teamed_sections])
        res='\t\tSection ID: {}\n\t\tPeriod: {}\n\t\tAllowed periods:{}\n\t\tSemester: {}\n\t\tMax student count: {}\n\t\tCourse(s): {}\n\t\tTeacher(s): {}\n\t\tRoom(s): {}\n\t\tStudent(s) ({}): {}'.format(self.id,self.period,allowed_pers,'year' if self.semester==0 else self.semester,self.maxstudents,courses,teachers,rooms,len(self.students),students)
        if self.teamed_sections:
            res+='\n\t\tTeamed with: '+teamedwith
        return res


    def __str__(self):
        return 'Section '+self.id

    def __repr__(self):
        return 'Section {}: {} {} P{} {}'.format(self.id,next(iter(self.teachers)).lastName if self.teachers else "Teacherless", next(iter(self.courses)).name if self.courses else "Courseless",self.period,"YR" if not self.semester else "S"+str(self.semester))

    def __hash__(self):
        return hash(object.__repr__(self))


class Student_Courses:
    def __init__(self,course_list,all_courses,alts=None):
        self.courses = set()
        self.alternates=set()
        if alts is not None:
            raise ValueError('Alternate courses not yet supported.')
        for i in course_list:
            i = i.strip()
            self.courses.add(all_courses[i])

    def to_str(self):
        cs='\n\t\t'.join(['']+[str(i) for i in self.courses]) if self.courses else '\n\t\tNone'
        alts='\n\t\t'.join(['']+self.alternates) if self.alternates else '\n\t\tNone'
        return '\tCourses:{}\n\tAlternates:{}'.format(cs,alts)







