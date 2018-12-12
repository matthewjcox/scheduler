from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
#from django.contrib.auth.decorators import login_required


from studentInput.models import Student, Category,Course
# Create your views here.
#@login_required()
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
        })
    return render(request, 'counselorEditor/editor.html', {
        'student': student.student_id,
        'course_list': student.student_course_request.all(),
        'category_list': Category.objects.all(),
    })

