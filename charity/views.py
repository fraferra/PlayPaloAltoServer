# Create your views here.
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
#from django.contrib.auth import authenticate, login as auth_login
from social_auth.models import UserSocialAuth
from play.models import *
from charity.models import *
from shop.models import *
from play.utils import *
from charity.utils import *
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.models import User
import json
from django.contrib.auth import logout as django_logout

from charity.forms import *

from django.core.exceptions import *
from datetime import datetime


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
            createEvent(request, organization)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/sorry/')
        return render(request, 'charity/organization_home.html', {'user':user,
                                                                  'player':player,
                                                                  'shop':shop})


    
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
            return render(request, 'charity/create_event.html', {'form':form,'shop':shop})
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
        return render(request, 'charity/my_events.html', {'list_of_events':list_of_events, 'number':number, 'shop':shop})
            


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
            Feed.objects.create(
                player=player,
                event=event,
                )
            player.score=player.score +  event.points
            player.experience=player.experience+event.experience
            player.event_set.remove(event)
            EventHistory.objects.create(
                date=datetime.today(),
                player=player,
                #event=event,
                organization=organization.title,
                title=event.title,
                event_type=event.event_type,
                points=event.points
                )
            player.save()
            event.save()
            return HttpResponseRedirect('/my_events/')


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
        return render(request, 'charity/my_company.html', {'user':user,'organization':organization, 'shop':shop})

