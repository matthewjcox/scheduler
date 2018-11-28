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
# Global vars:
_courses={}
_num_periods=7
course_file_name='courses.txt'
_course_creation_disabled= 1
_classrooms={}
_all_teachers={}
_all_students={}
_all_sections={}
# End global vars



class School:
    num_periods=_num_periods
    courses=_courses
    classrooms=_classrooms
    teachers=_all_teachers
    students=_all_students
    sections=_all_sections



class Teacher:
    def __init__(self, myLastName, myFirstName, teacherID, willTeach, keep_record=1):
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
        if keep_record:
            global _all_teachers
            _all_teachers[self.teacherID]=self

    def long_string(self):
        # courses=self.willTeach.to_str() if self.willTeach else '\n\tNone'
        schedule='\n\n'.join([i.long_string() for i in self.sched]) if self.sched else '\n\tNot yet assigned.'
        return f'{self.firstName} {self.lastName} ({self.teacherID})\n\tSchedule:\n{schedule}'

    def copy(self):
        return Teacher(self.lastName,self.firstName,self.teacherID, self.willTeach, keep_record=0)

    def __str__(self):
        return f'{self.firstName} {self.lastName} ({self.teacherID})'

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
        global _classrooms
        if roomNum not in _classrooms:
            _classrooms[roomNum]=Classroom(roomNum)
        return _classrooms[roomNum]

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

    @staticmethod
    def course(myID):
        if myID not in _courses:
            raise ReferenceError
            # courses[myID]=Course(myName, shortName, myID)
        return _courses[myID]

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
    def __init__(self,myLastName, myFirstName,myID,myCourses,keep_record=1):

        # studentID is a string that stores a student's student ID.
        self.studentID = myID

        self.firstName = myFirstName

        self.lastName = myLastName

        self.courses=myCourses#Student_Courses object

        # sched is a variable that holds an array of seven sections representing a student's schedule
        self.sched = set()
        if keep_record:
            global _all_students
            _all_students[self.studentID]=self

    def long_string(self):
        requests=self.courses.to_str() if self.courses else '\n\t\tNone'
        schedule='\n\t'.join(self.sched) if self.sched else '\n\t\tNot yet assigned.'
        return f'{self.firstName} {self.lastName} ({self.studentID})\nRequests:\n{requests}\nSchedule:{schedule}'

    def medium_string(self):
        requests = self.courses.to_str() if self.courses else '\n\t\tNone'
        sched='\n\t\t'.join([i.__repr__() for i in self.sched])
        return f'{requests}\n\tSchedule:\n\t\t{sched}'

    def __str__(self):
        return f'{self.firstName} {self.lastName} ({self.studentID})'


    def copy(self):
        return Student(self.lastName,self.firstName,self.studentID,self.courses,keep_record=0)

    def __hash__(self):
        return hash(self.studentID)

    def __eq__(self,other):
        return isinstance(other,Student) and self.studentID==other.studentID

class Section:
    def __init__(self, id, keep_record=1):
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
        self.allowed_periods=list(range(1,_num_periods+1))
        if keep_record:
            global _all_sections
            _all_sections[self.id]=self

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
        self.students.add(student)
        student.sched.add(self)

    def remove_student(self, student):
        if student not in self.students:
            raise ReferenceError
        self.students.remove(student)
        student.sched.remove(self)

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

    def set_allowed_periods(self,allowed_periods):
        self.allowed_periods=allowed_periods

    def space_available(self):
        return len(self.students)<=self.maxstudents-1

    def long_string(self):
        courses=", ".join([str(i) for i in self.courses])
        teachers = ", ".join([str(i) for i in self.teachers])
        rooms = ", ".join([str(i) for i in self.classrooms])
        students = ", ".join([str(i) for i in self.students])
        # periods=", ".join([str(i) for i in self.period])
        teamedwith=', '.join([str(i) for i in self.teamed_sections])
        res=f'\t\tSection ID: {self.id}\n\t\tPeriod: {self.period}\n\t\tMax student count: {self.maxstudents}\n\t\tCourse(s): {courses}\n\t\tTeacher(s): {teachers}\n\t\tRoom(s): {rooms}\n\t\tStudent(s) ({len(self.students)}): {students}'
        if self.teamed_sections:
            res+=f'\n\t\tTeamed with: {teamedwith}'
        return res


    def __str__(self):
        return f'Section {self.id}'

    def __repr__(self):
        return f'Section {self.id}: {next(iter(self.teachers)).lastName if self.teachers else "Teacherless"} {next(iter(self.courses)).name if self.courses else "Courseless"} P{self.period} {"YR" if not self.semester else "S"+str(self.semester)}'

    def __hash__(self):
        return hash(object.__repr__(self))


class Student_Courses:
    def __init__(self,course_list,alts=None):
        self.courses = set()
        self.alternates=set()
        if alts is not None:
            raise ValueError('Alternate courses not yet supported.')
        for i in course_list:
            i = i.strip()
            self.courses.add(Course.course(i))

    def to_str(self):
        cs='\n\t\t'.join(['']+[str(i) for i in self.courses]) if self.courses else '\n\t\tNone'
        alts='\n\t\t'.join(['']+self.alternates) if self.alternates else '\n\t\tNone'
        return f'\tCourses:{cs}\n\tAlternates:{alts}'

with open(course_file_name,'r') as f:
    for i in f:
        line=[j.strip() for j in i.split(',')]
        try:
            course=Course.create_new(*line)
        except:
            print(f'Error reading course: {line}')
            raise
        _courses[course.courseID]=course

with open('classrooms.txt','r') as f:
    for i in f:
        Classroom.classroom(i.strip())



