import requests
from django.contrib.auth.models import User,UserManager
from social_auth.models import UserSocialAuth
from django.contrib.auth import authenticate, login as auth_login
import json
from django.core.exceptions import *
from play.models import *
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
import string, random
def pictureUrl(user, player):
    try:
        social=UserSocialAuth.objects.get(user=user)
        if player.picture_url is None:
            token=social.extra_data['access_token']
            url = 'https://graph.facebook.com/me/?fields=id,name,picture&access_token='+token
            rr=requests.get(url).json()['picture']['data']['url']
            player.picture_url=rr
            player.save()
    except ObjectDoesNotExist:
        pass


def returnCustomUser(user):
    #from models import *
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
    #from play.models import *
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
'''

def customAuth(request):
    from play.models import *
    try:
        status=Player.objects.get(user=request.user).custom_auth
        return status
    except TypeError:
        return False
'''
