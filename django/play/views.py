# Create your views here.
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from social_auth.models import UserSocialAuth
from play.models import *
from play.utils import *

def login(request):
    return render(request, 'play/home.html')


def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    else:
    	user=request.user
    	customuser=returnCustomUser(user)
    	pictureUrl(customuser)
       
    	return render(request, 'play/home.html', {'customuser':customuser})
    	

def challenge(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    else:
        user=request.user
        customuser=returnCustomUser(user)
        return render(request)


def leaderboard(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    else:
        user=request.user
        customuser=returnCustomUser(user)
        return render(request)
	