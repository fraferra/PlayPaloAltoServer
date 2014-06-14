# Create your views here.
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
#from django.contrib.auth import authenticate, login as auth_login
from social_auth.models import UserSocialAuth
from play.models import *
from charity.models import *
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
    return render(request, 'general/index2.html', {'form':form})





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
        top10=Player.objects.order_by('experience').reverse()[:5]
        my_events=player.event_set.all()
        my_coupons=player.coupon_set.all()
        my_badges=player.badge_set.all()
        return render(request, 'play/tmp-home.html', {'user':user, 'player':player,
                                                 'num_events':num_events ,'my_coupons':my_coupons,
                                                 'top10':top10, 'my_events':my_events,
                                                 'my_badges':my_badges,
                                                 'organization':organization})

def look_events(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        my_events=player.event_set.all()
        organization, shop=getShop(user)
        events=returnEventChallengeDict()
        comment_events=[]
        yelp=findEvent()
        #for event in events:
            #comment_events.append((event, len(Comment.objects.filter(event=event))))
        id_event=request.GET.get('id_event','')
        if len(id_event)!=0:
            event=Event.objects.get(pk=id_event)
            if not event in my_events:
                event.participants.add(player)
                event.save()
                player.save()
                return HttpResponseRedirect('/home/')
        return render(request, 'play/tmp-look_event.html', {'user':user, 'player':player,
                                                 'events':events, 'my_events':my_events,
                                                 'yelp':yelp,
                                                 #'comment_events':comment_events,
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


def feeds(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        pictureUrl(user, player)
        organization, shop=getShop(user)
        feeds=Feed.objects.all().order_by('-date')
        coments_and_feeds=[]
        for feed in feeds:
            comments=CommentFeed.objects.filter(feed=feed).order_by('date')
            coments_and_feeds.append((feed, comments))
        id_comment_feed=request.POST.get('id_comment_feed','')
        if request.method=='POST':
            form = CommentFeedForm(request.POST) 
            if form.is_valid():
                new_comment = form.save(commit=False)
                feed_id=request.POST['feed_id']
                new_comment.feed=Feed.objects.get(id=feed_id)
                new_comment.commenter=player
                #new_comment.date=datetime.now
                new_comment.save()
        else:
            id_like_feed=request.GET.get('id_like_feed','')
            form=CommentFeedForm()
            if len(id_like_feed)!=0:
                addLike(id_like_feed)
                return HttpResponseRedirect('/feeds/')
        return render(request, 'play/feeds.html', {'user':user, 'player':player,
                                                    'form':form,
                                                    'coments_and_feeds':coments_and_feeds,
                                                 'organization':organization})



def edit_profile(request):
    completed_events=''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        player=Player.objects.get(user=user)
        completed_events=EventHistory.objects.filter(player=player)
        organization, shop=getShop(user)
        num_events=len(completed_events)
        top10=Player.objects.order_by('experience').reverse()[:5]
        my_badges=player.badge_set.all()
        if request.method=='POST':
            form2 = EditPicForm(request.POST, instance=player) 
            form = EditUserForm(request.POST, instance=user) 
            if form.is_valid() and form2.is_valid():
                updated_user = form.save()
                updated_pic=form2.save()
                print updated_pic.picture_url
                updated_pic.save()
                updated_user.save()
                return HttpResponseRedirect('/home/')
        else:
            form = EditUserForm(instance=user)
            form2 = EditPicForm( instance=player) 
        return render(request, 'play/edit_profile.html', {'user':user, 'player':player,
                                                          'num_events':num_events ,
                                                            'top10':top10,
                                                            'form2':form2,
                                                            'my_badges':my_badges,
                                                          'form':form,'organization':organization})

