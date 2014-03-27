# Create your views here.
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
#from django.contrib.auth import authenticate, login as auth_login
from social_auth.models import UserSocialAuth
from play.models import *
from play.utils import *
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
import json
@csrf_exempt
def login(request):
    username, password =authenticationFra(request)
    user = authenticate(username=username,  password=password)
    auth_login(request,user)
    if user.is_authenticated():
        player=Player.objects.get(user=user)

        data= {'user':user.username, 'player':player.score}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')
    else: 
        return HttpResponse('not auth')


@csrf_exempt
def leaderboard(request):
    username, password =authenticationFra(request)
    user = authenticate(username=username,  password=password)
    auth_login(request,user)
    if user.is_authenticated():
        player=Player.objects.get(user=user)
        players=Player.objects.all().order_by('score')
        list_of_players=[]
        for other_player in players:
            list_of_players.append(other_player.user.username)

        data= {'user':user.username, 'score':player.score, 'players':list_of_players}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')
    else: 
        pass

@csrf_exempt
def home(request):
    if not authenticationFra(request):
        return HttpResponse('/login')
    else:
        return HttpResponse('logged')
    '''
    user_id = request.GET['id']
    user=User.objects.get(pk=user_id)
    username = request.GET['username']
    user.username=username
    user.save()
    dump= {'user':user.username}
    data = simplejson.dumps(dump)
    return HttpResponse(data, mimetype='application/json')
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    else:
    	user=request.user
    	#customuser=returnCustomUser(user)
    	#pictureUrl(customuser)
        dump= {'user':user.username}
        data = simplejson.dumps(dump)
        return HttpResponse(data, mimetype='application/json')
    	#return render(request, 'play/home.html', {'customuser':customuser})
    	'''

def challenges(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    else:
        user=request.user
        customuser=returnCustomUser(user)
        return render(request)

def coupons(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    else:
        user=request.user
        customuser=returnCustomUser(user)
        return render(request)
        
def events(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    else:
        user=request.user
        customuser=returnCustomUser(user)
        return render(request)

	