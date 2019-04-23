#Matthew added this comment to test git updates
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Course, Category, Student


# Create your views here.
#@permission_required('counselorEditor.can_view')
#this one works better but I have no clue how it works
@login_required
def index(request):
    template = loader.get_template('studentInput/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
    """
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'studentInput/index.html', context)
    """
    
def course_selection(request):
    student = Student.objects.get(student_id = request.user.get_username())
    
    return render(request, 'studentInput/course_selection.html', {
        'student': student.student_id,
        #'course_list': student.student_course_request.all(),
        'course_list': [course.course_id for course in student.student_course_request.all()],
        'category_list': Category.objects.all(),
        'courseDict': Course.objects.all(),
        'numCourses': len(student.student_course_request.all()),
    })

def submit(request):
    try:
        student = Student.objects.get(student_id = request.POST['username'])
        courseRequestList = []
        for i in range(int(request.POST['numCourses'])):
            if request.POST['course'+str(i+1)] == 'empty':
                continue;
            courseRequestList.append(Course.objects.get(course_id = request.POST['course'+str(i+1)]))
        
        student.student_course_request.clear()
        for courseRequested in courseRequestList:
            student.student_course_request.add(courseRequested)
    except (KeyError, Student.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'studentInput/course_selection.html', {
            #'course_list': student.student_course_request.all(),
            'course_list': [request.POST['course'+str(i+1)] for i in range(int(request.POST['numCourses']))],
            'courseDict': Course.objects.all(),
            'category_list': Category.objects.all(),
            'student': request.user.get_username(),
            'error_message': "Your username doesn't exist :(",
            'numCourses': int(request.POST['numCourses']),
        })
    except (KeyError, Course.DoesNotExist):
        return render(request, 'studentInput/course_selection.html', {
            #'course_list': student.student_course_request.all(),
            'course_list': [request.POST['course'+str(i+1)] for i in range(int(request.POST['numCourses']))],
            'courseDict': Course.objects.all(),
            'category_list': Category.objects.all(),
            'student': request.user.get_username(),
            'error_message': "Invalid Course ID on Course " + str(i+1),
            'numCourses': int(request.POST['numCourses']),
        })
    else:
        student.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('studentInput:index'))

