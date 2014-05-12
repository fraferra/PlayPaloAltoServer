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
        top10=Player.objects.order_by('experience').reverse()[:10]
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
        events=Event.objects.all().order_by('date')
        comment_events=[]
        for event in events:
            comment_events.append((event, len(Comment.objects.filter(event=event))))
        id_event=request.GET.get('id_event','')
        if len(id_event)!=0:
            event=Event.objects.get(pk=id_event)
            if not event in my_events:
                event.participants.add(player)
                event.save()
                player.save()
                return HttpResponseRedirect('/home/')
        return render(request, 'play/look_events.html', {'user':user, 'player':player,
                                                 'events':events, 'my_events':my_events,
                                                 'comment_events':comment_events,
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
            if not coupon in my_coupons and player.score > 0 and coupon.coupons_released >0:
                coupon.buyers.add(player)
                coupon.coupons_released=coupon.coupons_released-1
                coupon.save()
                player.save()
                return HttpResponseRedirect('/home/')
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



def event(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        id_event=request.GET['id_event']
        event=Event.objects.get(pk=id_event)
        user=request.user
        player=Player.objects.get(user=user)
        organization, shop=getShop(user)
        previous_comments=Comment.objects.filter(event=event).order_by('date')
        if request.method=='POST':
            form = CommentForm(request.POST) 
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.commenter=player
                new_comment.event=event
                #new_comment.date=datetime.now
                new_comment.save()
                return HttpResponseRedirect('/event/?id_event='+id_event)
        else:
            form = CommentForm()

        return render(request, 'play/event.html', {'user':user, 'player':player,
                                                         'form':form,'event':event,
                                                         'previous_comments':previous_comments,
                                                  'organization':organization})

def wall(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        id_event=request.GET['id_event']
        event=Event.objects.get(pk=id_event)
        user=request.user
        player=Player.objects.get(user=user)
        organization, shop=getShop(user)

        return render(request, 'play/event.html', {'user':user, 'player':player,
                                                   'event':event,
                                                  'organization':organization}) 