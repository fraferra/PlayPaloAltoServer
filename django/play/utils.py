import requests

from social_auth.models import UserSocialAuth


def pictureUrl(customuser):
    if customuser.picture_url is None:
    	token=customuser.user.extra_data['access_token']
        url = 'https://graph.facebook.com/me/?fields=id,name,picture&access_token='+token
        rr=requests.get(url).json()['picture']['data']['url']
        customuser.picture_url=rr
        customuser.save()
    else:
        pass

def returnCustomUser(user):
    from models import *
    facebook_id=UserSocialAuth.objects.get(user=user).uid
    customuser=CustomUser.objects.get(facebook_id=facebook_id)
    return customuser