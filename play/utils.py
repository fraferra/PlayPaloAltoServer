import requests

from social_auth.models import UserSocialAuth


def pictureUrl(token):
    url = 'https://graph.facebook.com/me/?fields=id,name,picture&access_token='+token
    rr=requests.get(url).json()['picture']['data']['url']
    return rr

def returnCustomUser(user):
    from models import *
    facebook_id=UserSocialAuth.objects.get(user=user).uid
    customuser=CustomUser.objects.get(facebook_id=facebook_id)
    return customuser