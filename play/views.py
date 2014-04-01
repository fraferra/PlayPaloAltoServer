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

def home(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        User.objects.create(username=email, email=email, first_name=first_name,
                            last_name=last_name, password=password)
    return render(request, 'play/index.html')


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
            list_of_players.append({'player':other_player.user.username, 'player_experience':other_player.experience})

        data= {'user':user.username, 'score':player.score, 'players':list_of_players}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')
    else: 
        pass


@csrf_exempt
def coupons(request):
    username, password =authenticationFra(request)
    user = authenticate(username=username,  password=password)
    auth_login(request,user)
    if user.is_authenticated():
        player=Player.objects.get(user=user)
        #if request.method == 'GET':
        id_coupon=request.GET.get('id_coupon','')
        if len(id_coupon)!=0:
            coupon=Coupon.objects.get(pk=id_coupon)
            player.score=player.score-coupon.price
            if player.score <0:
                return HttpResponse('not enough points')
            coupon.buyers.add(player)
            coupon.save()
            player.save()
            data={'score':player.score}
            data = simplejson.dumps(data)
            return HttpResponse(data, mimetype='application/json')
        coupons=Coupon.objects.all()
        list_of_coupons=[]
        for cou in coupons:
            list_of_coupons.append({'name':cou.title, 'price':cou.price})
        data= {'user':user.username, 'list_of_coupons':list_of_coupons}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')
    else: 
        return HttpResponse('not auth')


@csrf_exempt
def my_coupons(request):
    username, password =authenticationFra(request)
    user = authenticate(username=username,  password=password)
    auth_login(request,user)
    if user.is_authenticated():
        player=Player.objects.get(user=user)
        coupons=player.coupon_set.all()
        list_of_coupons=[]
        for coupon in coupons:
            list_of_coupons.append({'name':coupon.title})
        data= {'user':user.username, 'player':player.score, 'coupons':list_of_coupons}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')
    else: 
        return HttpResponse('not auth') 

	