from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from requests_oauthlib import OAuth2Session
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scheduleServer.settings")
import django
django.setup()

from studentInput.models import Student,Course
# Create your views here.

    
CLIENT_ID = 'zN7yQ1B2w0mNFZBBAsHlEHk2KFLcxrKrJ0Dvu4cI'#aka the key
#^^SOCIAL_AUTH_ION_KEY^^ fix this later
CLIENT_SECRET = 'pYU4OqLzNBaRCqFsIJCt31qCVQcJ0xNa6apmOEFZ3Y77BTJvjuvMkCsdoGgcV2htbL8RkodS37Lt2fo4QHGniJ75VDDscjSJPBw4wNVWShWReTtgweMmRO54mx4oOt7x'
#^^SOCIAL_AUTH_ION_SECRET^^ fix this later
REDIRECT_URI = 'https://schedule.sites.tjhsst.edu/loginPage/redirect'
oauth = OAuth2Session(CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scope=["read","write"])
        
def index(request):
    oauth = OAuth2Session(CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scope=["read","write"])
    authorization_url, state = oauth.authorization_url("https://ion.tjhsst.edu/oauth/authorize/")
    
    #return render(request, 'loginPage/index.html')
    
    return HttpResponseRedirect(reverse('social:begin', args=['Ion']))
    

def redirect(request):
    token = oauth.fetch_token("https://ion.tjhsst.edu/oauth/token/",
        code=request.GET.get('code'),
        client_secret=CLIENT_SECRET)
    try:
        profile = oauth.get("https://ion.tjhsst.edu/api/profile")
    except TokenExpiredError as e:
        args = { "client_id": 'CLIENT_ID', "client_secret": CLIENT_SECRET }
        token = oauth.refresh_token("https://ion.tjhsst.edu/oauth/token/", **args)
        #return HttpResponseRedirect(reverse('loginPage:index'))
    
    info = json.loads(profile.content.decode())
    """
    return render(request, 'loginPage/info.html',{
        'info':info
    })
    """
    user = authenticate(username = info['ion_username'], password = '12345')
    if user is None:
        user = User.objects.create_user(info['ion_username'], info['tj_email'],'12345')
        student = Student.objects.create( student_id = info['ion_username'], 
                                student_first_name = info['first_name'], 
                                student_last_name = info['last_name'])
        for i in {'000001','000002','000003','000004','000005','000006','000007'}:
            student.student_course_request.add(Course.objects.get(course_id = i))
    request.session.set_expiry(86400)
    user.first_name = info['first_name']
    user.last_name = info['last_name']
    login(request,user)
    return HttpResponseRedirect(reverse('projectIndex:'+info['user_type']))



