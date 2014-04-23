# Create your views here.
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
#from django.contrib.auth import authenticate, login as auth_login
from social_auth.models import UserSocialAuth
from play.models import *
from play.utils import *
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.models import User
import json
from django.contrib.auth import logout as django_logout
from play.forms import *
from django.core.exceptions import *

#API




def api_registration(request):
    if request.method == 'GET':
        email = request.GET['email']
        first_name=request.GET['first_name']
        last_name=request.GET['last_name']
        password = request.GET['password']
        user=User.objects.create(username=email, email=email, 
                            first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return HttpResponseRedirect('/api/login/')









def api_v2_login(request):
    message='not auth'
    data={'message':message}
    username = request.GET.get('username','')
    password = request.GET.get('password','')
    user = authenticate(username =username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            player=Player.objects.get(user=user)
            player.token=randomword(30)
            player.save()
            data= {'token':player.token}
            data = simplejson.dumps(data)
            #message='logged in successfully'
            return HttpResponse(data, mimetype='application/json')
        else:
            message='not authenticated'
    else:
        message='not existing'
    data=simplejson.dumps(data)
    response = HttpResponse(data, mimetype='application/json')   
    response.set_cookie('user', user)
    return response



def api_v2_logout(request):
    player=Player.objects.get(user=request.user)
    player.token=''
    player.save()
    django_logout(request)
    return HttpResponseRedirect('/api/v2/login/')


 

def api_v2_home(request):
    if not customAuth(request):
        return HttpResponseRedirect('/api/v2/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        pictureUrl(user, player)
        data= {'user':user.username, 'score':player.score, 'experience':player.experience, 'picture_url':player.picture_url}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')   


def api_v2_leaderboard(request):
    if not customAuth(request):
        return HttpResponseRedirect('/api/v2/login/')
    else:
        token=request.GET.get('token','')
        player=Player.objects.get(token=token)
        user=player.user

        players=Player.objects.all().order_by('score')
        list_of_players=[]
        for other_player in players:
            list_of_players.append({'player':other_player.user.username, 'player_experience':other_player.experience})

        data= {'user':user.username, 'score':player.score, 'experience':player.experience,
                'picture_url':player.picture_url, 'players':list_of_players}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')

def api_v2_my_events(request):
    if not customAuth(request):
        return HttpResponseRedirect('/api/v2/login/')
    else:
        token=request.GET.get('token','')
        player=Player.objects.get(token=token)
        user=player.user
        events=player.event_set.all()
        list_events=[]
        for event in events:
            list_events.append({'name':event.title, 'points':event.points, 'experience':event.experience, 'location':event.location})
        data= {'user':user.username, 'score':player.score, 'experience':player.experience,
               'picture_url':player.picture_url, 'events':list_events}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')


def api_v2_my_coupons(request):
    if not customAuth(request):
        return HttpResponseRedirect('/api/v2/login/')
    else:
        token=request.GET.get('token','')
        player=Player.objects.get(token=token)
        user=player.user
        coupons=player.coupon_set.all()
        list_coupons=[]
        id_coupon=request.GET.get('id','')
        if len(id_coupon)!=0:
            my_coupon=Coupon.objects.get(id=id_coupon)
            player.coupon_set.remove(my_coupon)
            data={'message':'Coupon redeemed!'}
            data = simplejson.dumps(data)
            return HttpResponse(data, mimetype='application/json')           
        for coupon in coupons:
            list_events.append({'name':coupon.title, 'points':coupon.points, 'location':coupon.location, 'shop':coupon.shop})
        data= {'user':user.username, 'score':player.score, 'experience':player.experience, 
               'picture_url':player.picture_url, 'coupons':list_coupons}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')



def api_v2_coupons(request):
    if not customAuth(request):
        return HttpResponseRedirect('/api/v2/login/')
    else:
        token=request.GET.get('token','')
        player=Player.objects.get(token=token)
        user=player.user
        id_coupon=request.GET.get('id','')
        if len(id_coupon)!=0:
            coupon=Coupon.objects.get(pk=id_coupon)
            player.score=player.score-coupon.price
            coupons=player.coupon_set.all()
            if coupon in coupons:
                data={'message':'You have already selected!'}
                data = simplejson.dumps(data)
                return HttpResponse(data, mimetype='application/json')
            else:
                if player.score <0:
                    data={'message':'Not enough points'}
                    data = simplejson.dumps(data)
                    return HttpResponse(data, mimetype='application/json')
                coupon.buyers.add(player)
                coupon.save()
                player.save()
                data={'score':player.score}
                data = simplejson.dumps(data)
                return HttpResponse(data, mimetype='application/json')
        coupons=Coupon.objects.all()
        list_of_coupons=[]
        for cou in coupons:
            list_of_coupons.append({'name':cou.title, 'price':cou.price, 'location':cou.location, 'shop':cou.shop})
        data= {'user':user.username, 'score':player.score, 'experience':player.experience, 
               'picture_url':player.picture_url, 'list_of_coupons':list_of_coupons}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')

def api_v2_events(request):
    if not customAuth(request):
        return HttpResponseRedirect('/api/v2/login/')
    else:
        token=request.GET.get('token','')
        player=Player.objects.get(token=token)
        user=player.user
        id_event=request.GET.get('id','')
        if len(id_event)!=0:
            event=Event.objects.get(pk=id_event)
            events=player.event_set.all()
            if not event in events:
                event.participants.add(player)
                event.save()
                player.save()
                data={'event':event.title}
                data = simplejson.dumps(data)
                return HttpResponse(data, mimetype='application/json')
            else:
                data={'message':'You have already selected!'}
                data = simplejson.dumps(data)
                return HttpResponse(data, mimetype='application/json')                
        events=Event.objects.all()
        list_events=[]
        for eve in events:
            list_events.append({'name':eve.title, 'location':eve.location, 'points':eve.points, 'experience':eve.experience})
        data= {'user':user.username, 'score':player.score, 'experience':player.experience, 
               'picture_url':player.picture_url, 'list_events':list_events}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')







def api_v1_logout(request):
    django_logout(request)
    return HttpResponseRedirect('/api/login/')

def api_v1_login(request):
    message=''
    data={'message':message}
    username = request.GET.get('username','')
    password = request.GET.get('password','')
    user = authenticate(username =username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)

            #message='logged in successfully'
            return HttpResponseRedirect('/api/v1/home/')
        else:
            message='not authenticated'
    else:
        message='not existing'
    data=simplejson.dumps(data)
    return HttpResponse(data, mimetype='application/json')

 

def api_v1_home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/api/v1/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        pictureUrl(user, player)
        data= {'user':user.username, 'score':player.score, 'experience':player.experience, 'picture_url':player.picture_url}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')   


def api_v1_leaderboard(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/api/v1/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        players=Player.objects.all().order_by('score')
        list_of_players=[]
        for other_player in players:
            list_of_players.append({'player':other_player.user.username, 'player_experience':other_player.experience})

        data= {'user':user.username, 'score':player.score, 'experience':player.experience,
                'picture_url':player.picture_url, 'players':list_of_players}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')

def api_v1_my_events(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/api/v1/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        events=player.event_set.all()
        list_events=[]
        for event in events:
            list_events.append({'name':event.title, 'points':event.points, 'experience':event.experience, 'location':event.location})
        data= {'user':user.username, 'score':player.score, 'experience':player.experience,
               'picture_url':player.picture_url, 'events':list_events}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')


def api_v1_my_coupons(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/api/v1/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        coupons=player.coupon_set.all()
        list_coupons=[]
        id_coupon=request.GET.get('id','')
        if len(id_coupon)!=0:
            my_coupon=Coupon.objects.get(id=id_coupon)
            player.coupon_set.remove(my_coupon)
            data={'message':'Coupon redeemed!'}
            data = simplejson.dumps(data)
            return HttpResponse(data, mimetype='application/json')           
        for coupon in coupons:
            list_events.append({'name':coupon.title, 'points':coupon.points, 'location':coupon.location, 'shop':coupon.shop})
        data= {'user':user.username, 'score':player.score, 'experience':player.experience, 
               'picture_url':player.picture_url, 'coupons':list_coupons}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')



def api_v1_coupons(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/api/v1/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        id_coupon=request.GET.get('id','')
        if len(id_coupon)!=0:
            coupon=Coupon.objects.get(pk=id_coupon)
            player.score=player.score-coupon.price
            coupons=player.coupon_set.all()
            if coupon in coupons:
                data={'message':'You have already selected!'}
                data = simplejson.dumps(data)
                return HttpResponse(data, mimetype='application/json')
            else:
                if player.score <0:
                    data={'message':'Not enough points'}
                    data = simplejson.dumps(data)
                    return HttpResponse(data, mimetype='application/json')
                coupon.buyers.add(player)
                coupon.save()
                player.save()
                data={'score':player.score}
                data = simplejson.dumps(data)
                return HttpResponse(data, mimetype='application/json')
        coupons=Coupon.objects.all()
        list_of_coupons=[]
        for cou in coupons:
            list_of_coupons.append({'name':cou.title, 'price':cou.price, 'location':cou.location, 'shop':cou.shop})
        data= {'user':user.username, 'score':player.score, 'experience':player.experience, 
               'picture_url':player.picture_url, 'list_of_coupons':list_of_coupons}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')

def api_v1_events(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/api/v1/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        id_event=request.GET.get('id','')
        if len(id_event)!=0:
            event=Event.objects.get(pk=id_event)
            events=player.event_set.all()
            if not event in events:
                event.participants.add(player)
                event.save()
                player.save()
                data={'event':event.title}
                data = simplejson.dumps(data)
                return HttpResponse(data, mimetype='application/json')
            else:
                data={'message':'You have already selected!'}
                data = simplejson.dumps(data)
                return HttpResponse(data, mimetype='application/json')                
        events=Event.objects.all()
        list_events=[]
        for eve in events:
            list_events.append({'name':eve.title, 'location':eve.location, 'points':eve.points, 'experience':eve.experience})
        data= {'user':user.username, 'score':player.score, 'experience':player.experience, 
               'picture_url':player.picture_url, 'list_events':list_events}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')



