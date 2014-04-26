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
from datetime import datetime
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



def idea(request):
    if request.method=='POST':
        form = IdeaForm(request.POST) 
        if form.is_valid():
            new_idea = form.save()
            return HttpResponseRedirect('/') 
    else:
        form = IdeaForm()
    return render(request, 'play/idea.html', {'form':form})


def index(request):
    if request.method=='POST':
        form = SignUpForm(request.POST) 
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/login/') 
    else:
        form = SignUpForm()
    return render(request, 'play/index.html', {'form':form})


def organization_home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        pictureUrl(user, player)
        organization, shop =getShop(user)
        try:
            organization=Organization.objects.get(user=user)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/sorry/')
        return render(request, 'play/organization_home.html', {'user':user, 'player':player, 'shop':shop})


    
def sorry(request):
    return render(request, 'play/sorry.html')

def create_event(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        organization, shop=getShop(user)
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
            return render(request, 'play/create_event.html', {'form':form,'shop':shop})
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/sorry/')


def create_coupon(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user

        try:
            #organization=Organization.objects.get(user=user)
            organization, shop=getShop(user)
            if request.method=='POST':
                form = CouponForm(request.POST) 
                if form.is_valid():
                    new_coupon = form.save(commit=False)
                    new_coupon.shop=shop
                    new_coupon.save()
                    return HttpResponseRedirect('/my_coupons/')
            else:
                form = CouponForm()
            return render(request, 'play/create_coupon.html', {'form':form, 'shop':shop})
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/sorry/')

def my_events(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        organization, shop=getShop(user)
        if not organization: 
            return HttpResponseRedirect('/sorry/')
        list_of_events=Event.objects.filter(organizer=organization)
        number=len(list_of_events)
        id_delete=request.GET.get('delete','')
        if len(id_delete)!=0:
            event=Event.objects.get(pk=id_delete)
            event.delete()
            return HttpResponseRedirect('/my_events/')
        return render(request, 'play/my_events.html', {'list_of_events':list_of_events, 'number':number, 'shop':shop})
            

def my_coupons(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        organization, shop=getShop(user)
        if not organization:
            return HttpResponseRedirect('/sorry/')
        list_of_coupons=Coupon.objects.filter(shop=shop)
        number=len(list_of_coupons)
        id_delete=request.GET.get('delete','')
        if len(id_delete)!=0:
            coupon=Coupon.objects.get(pk=id_delete)
            coupon.delete()
            return HttpResponseRedirect('/my_coupons/')
        return render(request, 'play/my_coupons.html', {'list_of_coupons':list_of_coupons, 'number':number, 'shop':shop})



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
            EventHistory.objects.create(
                date=datetime.today(),
                player=player,
                #event=event,
                organization=organization.title,
                title=event.title,
                points=event.points
                )
            player.save()
            event.save()
            return HttpResponseRedirect('/my_events/')

def erase(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        organization, shop=getShop(user)
        if request.method == 'GET':
            id_user=request.GET['id_user']
            id_coupon=request.GET['id_coupon']
            coupon=Coupon.objects.get(id=id_coupon)
            player=Player.objects.get(id=id_user)
            player.coupon_set.remove(coupon)
            CouponHistory.objects.create(
                player=player,
                shop=shop.title,
                title=coupon.title,
                #coupon=coupon
                )
            player.save()
            coupon.save()
            return HttpResponseRedirect('/my_coupons/')

def my_company(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        organization, shop=getShop(user)
        if not organization:
            return HttpResponseRedirect('/sorry/')
        if request.method=='POST':
            title=request.POST.get('title', '')
            location=request.POST.get('location','')
            organization.title=title
            organization.location=location
            organization.save()
            return HttpResponseRedirect('/company/')
        return render(request, 'play/my_company.html', {'user':user,'organization':organization, 'shop':shop})

#USER PAGES


def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        pictureUrl(user, player)
        organization, shop=getShop(user)
        completed_events=EventHistory.objects.filter(player=player)
        num_events=len(completed_events)
        top10=Player.objects.order_by('experience')[10:]
        my_events=player.event_set.all()
        my_coupons=player.coupon_set.all()
        return render(request, 'play/home.html', {'user':user, 'player':player,
                                                 'num_events':num_events ,'my_coupons':my_coupons,
                                                 'top10':top10, 'my_events':my_events,
                                                 'organization':organization})

def look_events(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        my_events=player.event_set.all()
        organization, shop=getShop(user)
        events=Event.objects.all()
        id_event=request.GET.get('id_event','')
        if len(id_event)!=0:
            event=Event.objects.get(pk=id_event)
            if not event in my_events:
                event.participants.add(player)
                event.save()
                player.save()
        return render(request, 'play/look_events.html', {'user':user, 'player':player,
                                                 'events':events, 'my_events':my_events,
                                                 'organization':organization})

def look_coupons(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        my_coupons=player.coupon_set.all()
        organization, shop=getShop(user)
        coupons=Coupon.objects.all()
        id_coupon=request.GET.get('id_coupon','')
        if len(id_coupon)!=0:
            coupon=Coupon.objects.get(pk=id_coupon)
            player.score = player.score - coupon.price
            if not coupon in my_coupons or player.score > 0 :
                coupon.buyers.add(player)
                coupon.save()
                player.save()
        return render(request, 'play/look_coupons.html', {'user':user, 'player':player,
                                                 'coupons':coupons, 'my_coupons':my_coupons,
                                                 'organization':organization})


def leaderboard(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        organization, shop=getShop(user)
        sorted_list=Player.objects.order_by('experience').reverse()
        length=len(sorted_list)
        player_position = 0
        i=1
        lis=[]
        for p in sorted_list:
            lis.append((i, p))
            if player == p:
                player_position=i
            i=i+1
        return render(request, 'play/leaderboard.html', {'user':user, 'player':player,'length':length,'lis':lis,
                                                  'sorted_list':sorted_list, 'player_position':player_position,
                                                  'organization':organization})
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

#v2


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

def api_v2_history_events(request):
    if not customAuth(request):
        return HttpResponseRedirect('/api/v2/login/')
    else:
        token=request.GET.get('token','')
        player=Player.objects.get(token=token)
        user=player.user
        events=EventHistory.objects.filter(player=player)
        list_events=[]
        for event in events:
            list_events.append({'name':event.title, 'points':event.points, 'organization':event.organization })
        data= {'user':user.username, 'score':player.score, 'experience':player.experience,
               'picture_url':player.picture_url, 'events':list_events}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')

def api_v2_history_coupons(request):
    if not customAuth(request):
        return HttpResponseRedirect('/api/v2/login/')
    else:
        token=request.GET.get('token','')
        player=Player.objects.get(token=token)
        user=player.user
        events=CouponHistory.objects.filter(player=player)
        list_events=[]
        for event in events:
            list_events.append({'name':event.title, 'shop':event.shop })
        data= {'user':user.username, 'score':player.score, 'experience':player.experience,
               'picture_url':player.picture_url, 'events':list_events}
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





#v1

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

def api_v1_history_events(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/api/v1/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        events=EventHistory.objects.filter(player=player)
        list_events=[]
        for event in events:
            list_events.append({'name':event.title, 'points':event.points,  'organization':event.organization})
        data= {'user':user.username, 'score':player.score, 'experience':player.experience,
               'picture_url':player.picture_url, 'events':list_events}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')

def api_v1_history_coupons(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/api/v1/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        events=CouponHistory.objects.filter(player=player)
        list_events=[]
        for event in events:
            list_events.append({'name':event.title, 'shop':event.shop})
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



