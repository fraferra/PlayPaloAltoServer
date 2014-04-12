import requests
from django.contrib.auth.models import User,UserManager
from social_auth.models import UserSocialAuth
from django.contrib.auth import authenticate, login as auth_login
import json
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
    from models import *
    facebook_id=UserSocialAuth.objects.get(user=user).uid
    customuser=CustomUser.objects.get(facebook_id=facebook_id)
    return customuser

def authenticationFra(request):
    result=request.body
    result = json.loads(result)
    username=result['username']
    password=result['password']
    return username, password
