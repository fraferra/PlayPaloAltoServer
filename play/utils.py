import requests

def pictureUrl(token):
    url = 'https://graph.facebook.com/me/?fields=id,name,picture&access_token='+token
    rr=requests.get(url).json()['picture']['data']['url']
    return rr