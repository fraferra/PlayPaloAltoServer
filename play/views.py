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

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username =username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/home/')
    return render(request, 'play/login.html')


def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/login/')



def index(request):
    if request.method=='POST':
        form = SignUpForm(request.POST) 
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/login/') 
    else:
        form = SignUpForm()
    return render(request, 'play/index.html', {'form':form})


def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        try:
            organization=Organization.objects.get(user=user)
            return render(request, 'play/home.html', {'user':user})
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/sorry/')

    
def sorry(request):
    return render(request, 'play/sorry.html')

def create_event(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        try:
            organization=Organization.objects.get(user=user)
            if request.method=='POST':
                form = EventForm(request.POST) 
                if form.is_valid():
                    new_event = form.save(commit=False)
                    new_event.organizer=organization
                    new_event.save()
                    return HttpResponseRedirect('/my_events/')
            else:
                form = EventForm()
            return render(request, 'play/create_event.html', {'form':form})
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/sorry/')

def my_events(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        try:
            organization=Organization.objects.get(user=user)
            list_of_events=Event.objects.filter(organizer=organization)
            number=len(list_of_events)
            id_delete=request.GET.get('delete','')
            if len(id_delete)!=0:
                event=Event.objects.get(pk=id_delete)
                event.delete()
                return HttpResponseRedirect('/my_events/')
            return render(request, 'play/my_events.html', {'list_of_events':list_of_events, 'number':number})
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/sorry/')



def reward(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        organization=Organization.objects.get(user=user)
        if request.method == 'GET':
            id_user=request.GET['id_user']
            id_event=request.GET['id_event']
            event=Event.objects.get(id=id_event)
            player=Player.objects.get(id=id_user)
            player.score=player.score +  event.points
            player.experience=player.experience+event.experience
            player.event_set.remove(event)
            player.save()
            event.save()
            return HttpResponseRedirect('/my_events/')


def my_company(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        try:
            organization=Organization.objects.get(user=user)
            if request.method=='POST':
                title=request.POST.get('title', '')
                location=request.POST.get('location','')
                organization.title=title
                organization.location=location
                organization.save()
                return HttpResponseRedirect('/company/')
            return render(request, 'play/my_company.html', {'user':user,'organization':organization})
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/sorry/')


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

def api_logout(request):
    django_logout(request)
    return HttpResponseRedirect('/api/login/')

def api_login(request):
    message=''
    data={'message':message}
    username = request.GET.get('username','')
    password = request.GET.get('password','')
    user = authenticate(username =username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)

            #message='logged in successfully'
            return HttpResponseRedirect('/api/home/')
        else:
            message='not authenticated'
    else:
        message='not existing'
    data=simplejson.dumps(data)
    return HttpResponse(data, mimetype='application/json')

def api_home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/api/login/')
    else:
        user=request.user
        data= {'user':user.username, 'score':player.score, 'experience':player.experience, 'picture_url':player.picture_url}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')   


def api_leaderboard(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/api/login/')
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

def api_my_events(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/api/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        events=player.event_set.all()
        list_events=[]
        for event in events:
            list_events.append({'name':event.title, 'points':event.points, 'experience':event.experience, 'location':event.location})
        data= {'user':user.username, 'score':player.score, 'experience':player.experience,
               'picture_url':player.picture_url 'events':list_events}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')


def api_my_coupons(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/api/login/')
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



def api_coupons(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/api/login/')
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

def api_events(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/api/login/')
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





'''

@csrf_exempt
def api_login(request):
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


'''

	