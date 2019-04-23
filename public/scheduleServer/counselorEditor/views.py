from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import os.path



from studentInput.models import Student, Category,Course, Teacher, Room, Section
# Create your views here.
@login_required()
def index(request):
    template = loader.get_template('counselorEditor/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def search(request):
    return render(request, 'counselorEditor/search.html')

def edit(request):
    try:
        student = Student.objects.get(student_id = request.POST['username'])
    except (KeyError, Student.DoesNotExist):
        return render(request, 'counselorEditor/search.html', {
            'error_message': "User not found",
            'username': request.POST['username']
        })
    
    return render(request, 'counselorEditor/editor.html', {
        'student': student.student_id,
        'course_list': [course.course_id for course in student.student_course_request.all()],
        'category_list': Category.objects.all(),
        'courseDict': Course.objects.all(),
        'username': request.POST['username'],
        'numCourses': len(student.student_course_request.all()),
    })

def submit(request):
    try:
        student = Student.objects.get(student_id = request.POST['username'])
        courseRequestList = []
        for i in range(int(request.POST['numCourses'])):
            courseRequestList.append(Course.objects.get(course_id = request.POST['course'+str(i+1)]))
        
        student.student_course_request.clear()
        for courseRequested in courseRequestList:
            student.student_course_request.add(courseRequested)
    except (KeyError, Course.DoesNotExist):
        return render(request, 'counselorEditor/editor.html', {
            'student': student.student_id,
            'course_list': student.student_course_request.all(),
            'category_list': Category.objects.all(),
            'courseDict': Course.objects.all(),
            'error_message': "Invalid CourseID",
            'numCourses': request.POST['numCourses'],
        })
    else:
        student.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('counselorEditor:search'))


def upload(request):
    return render(request,'counselorEditor/upload.html',{
        'error_message': '',
    })
    
def success(request):
    inFile = request.FILES.get('parameters',False)
    if inFile.multiple_chunks():
        return render(request,'counselorEditor/upload.html',{
        'error_message': 'Error: File size too large',
    })
    outFile = open('../../private/parameters.txt','w+')
    data = inFile.read()
    print("data:\n")
    print(data)
    outFile.write(data.decode())
    outFile.close()
    return HttpResponseRedirect(reverse('counselorEditor:index'))#success
    
def sections(request):
    return render(request,'counselorEditor/sections.html',{
        'teacher_list':sorted(list(Teacher.objects.all()), key = lambda teacher: teacher.teacher_id),
        'room_list':sorted(list(Room.objects.all()), key = lambda room: room.rmNum),
        'course_list': sorted(list(Course.objects.all()), key = lambda course: course.course_id),
    })
    
def input_sections(request):
    
    course = Course.objects.get(course_id =  request.POST['course'])
    """
    return render(request, "counselorEditor/info.html", {
        'info': request.POST,
        })
    #"""
    for num in request.POST.getlist('period'):
        c = course.section_set.create(
            #section_id = courseID-number,
            section_id = request.POST['course'] + "-" + str(len(course.section_set.all())),
            room = Room.objects.get(rmNum = request.POST['room']),
            students_num_max = request.POST['numStudent'],
            period = num,
        )
        for teacher in request.POST.getlist('teacher'):
            c.teachers.add(Teacher.objects.get(teacher_id = teacher))
    
    return HttpResponseRedirect(reverse('counselorEditor:sections'))
    
def relation(request):
    return render(request, "counselorEditor/relation.html",{
        'section_list': [{'section':section.section_id,'course':Course.objects.get(section__section_id = section.section_id).course_name} for section in Section.objects.all()],
    })
    
def big_button(request):
    return render(request, 'counselorEditor/start.html')
    
def start(request):
    return HttpResponseRedirect(reverse('counselorEditor:index'))