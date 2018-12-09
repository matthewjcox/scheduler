from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
# Create your views here.

import re
from django.apps import apps
from scheduleServer.settings import MY_APPS

def index(request):
    app_list = [re.match("^.*?(?=\.)",appName).group(0) for appName in MY_APPS]
    template = loader.get_template('projectIndex/index.html')
    for index in range(len(app_list)):
        app_list[index] += ":index"
    
    context = {
        'app_list': app_list,
    }
    return HttpResponse(template.render(context, request))
    
def redirect(request, appName):
    return 