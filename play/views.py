# Create your views here.
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from social_auth.models import UserSocialAuth
from play.models import *
def home(request):
    return render(request, 'play/home.html')

def test(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
    	user=request.user
    	customuser=returnCustomUser(user)

    	return HttpResponse(customuser)