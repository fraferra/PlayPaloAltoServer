import requests
from django.contrib.auth.models import User,UserManager
from social_auth.models import UserSocialAuth
from django.contrib.auth import authenticate, login as auth_login
import json
from play.models import *
from charity.models import *
from shop.models import *
from django.core.exceptions import *
#from play.models import *
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
import string, random
from datetime import *

from bs4 import BeautifulSoup
import re

def pictureUrl(user, player):
    try:
        social=UserSocialAuth.objects.get(user=user)
        if player.facebook_pic is True:
            social.refresh_token()
            token=social.extra_data['access_token']
            url = 'https://graph.facebook.com/me/?fields=id,name,picture&access_token='+token
            rr=requests.get(url).json()['picture']['data']['url']
            player.picture_url=rr
            player.save()
    except ObjectDoesNotExist:
        pass


def returnCustomUser(user):
    from play.models import CustomUser
    facebook_id=UserSocialAuth.objects.get(user=user).uid
    customuser=CustomUser.objects.get(facebook_id=facebook_id)
    return customuser

def authenticationFra(request):
    result=request.body
    result = json.loads(result)
    username=result['username']
    password=result['password']
    return username, password



def customAuth(request):
    from play.models import Player
    token=''
    try:
        token=request.GET.get('token','')
        if len(token)!=0:
            try:
                player=Player.objects.get(token=token)
                return True
            except ObjectDoesNotExist:
                return False
        else:
            return False
    except TypeError:
        return False

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def getShop(user):
    from play.models import Shop, Organization
    try:
        shop = Shop.objects.get(user=user)
    except ObjectDoesNotExist:
        shop = False
    try:
        organization = Organization.objects.get(user=user)
    except ObjectDoesNotExist:
        organization = False
    return organization, shop



def addLike(id_like_feed):
    from play.models import Feed
    feed=Feed.objects.get(pk=id_like_feed)
    feed.likes=feed.likes+1
    feed.save()
'''
def addComment(id_comment_feed, comment, player):
    feed=Feed.objects.get(pk=id_comment_feed)
    CommentFeed.objects.create(
        comment=comment,
        commenter=player,
        feed=feed,
        )'''



def returnEventChallengeDict(*args):
    from play.models import Event,Player
    if len(args)!=0:
        events=args[0].event_set.all().order_by('-date')
    else:
        events=Event.objects.all().order_by('-date')
    today_events=[]
    past_events=[]
    future_events=[]
    challenges=[]
    today=date.today()
    for event in events:
        if event.challenge_event =='Event':
            if event.date.date() == today:
                today_events.append(event)
            if event.date.date() < today:
                past_events.append(event)
            else:
                future_events.append(event)
        else:
            challenges.append(event)
    return {'past':past_events, 'today':today_events,
                     'future':future_events, 'challenges':challenges}


def findEvent():   
    url='http://www.yelp.com/events/palo-alto'
    event_page=BeautifulSoup(requests.get(url).text)
    links=[]
    popular_events_div = event_page.find(id="popular_events")
    liks_h3 = event_page.find_all('h3')
    for t in liks_h3:
        t2= t.find('a')
        if not t2 is None:
            #print t2
            #print t2.find('span').text
            links.append((t2.find('span').text, t2['href']))
    return links
