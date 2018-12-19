from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
#from django.contrib.auth.decorators import login_required
import os.path


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