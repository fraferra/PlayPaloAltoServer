# Create your views here.
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login

def home(request):
    return render(request, 'play/home.html')

def test(request):
    if not request.user.is_authenticated():
        return HttpResponse('Hello')
    else:
    	return HttpResponse('auth@!!')