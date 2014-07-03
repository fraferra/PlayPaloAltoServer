# Create your views here.
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
#from django.contrib.auth import authenticate, login as auth_login
from social_auth.models import UserSocialAuth
from play.models import *
from charity.models import *
from shop.models import *
from play.utils import *
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.models import User
import json
from django.contrib.auth import logout as django_logout

from charity.forms import *

from django.core.exceptions import *
from datetime import datetime

def createEvent(request, organization):
	if request.method=='POST':
		title=request.POST.get('title','')
		description=request.POST.get('description','')
		challenge_event=request.POST.get('challenge_event','')
		points=request.POST.get('points','')
		experience=request.POST.get('experience','')
		event_type=request.POST.get('event_type','')
		date=request.POST.get('date','')
		location=request.POST.get('location','')
		Event.objects.create(
			title=title,
			description=description,
			challenge_event=challenge_event,
			experience=experience,
			points=points,
			date=date,
			organizer=organization,
			event_type=event_type,
			location=location,
			)
		return HttpResponseRedirect('/organization_home/')
