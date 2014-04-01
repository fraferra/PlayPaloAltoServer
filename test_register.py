import requests
import json
from urllib2 import urlopen
import datetime
import simplejson
from requests.auth import HTTPBasicAuth
import sys
method=sys.argv[1]

print method
if method=='user':
    #url = 'http://127.0.0.1:8000/api/v1/newuser/'
    url='http://www.playpaloalto.com/api/v1/newuser/'
    data = {'username' :'test2', 'password' : '1', 'email':'test@gmail.com', 'first_name':'fra'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    print json.dumps(data)
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print r.content

if method=='player':
    url = 'http://127.0.0.1:8000/api/v1/player/2/'
    data = {'score' :'12', 'user':'/api/v1/user/2/'}
    auth=('test', '1')
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    print json.dumps(data)
    r = requests.put(url, data=json.dumps(data), headers=headers, auth=auth)
    print r.content    

if method=='coupon':
    url = 'http://127.0.0.1:8000/api/v1/coupon/1/'
    data = {'buyers':["/api/v1/player/1/"], 'price':'12'}
    #data = {'price':'12'}
    auth=('fraferra', '1')
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    print json.dumps(data)
    r = requests.put(url, data=json.dumps(data), headers=headers, auth=auth)
    print r.content    

if method=='login':
    url = 'http://127.0.0.1:8000/play/login/'
    #data = {'buyers':["/api/v1/player/1/"], 'price':'12'}
    #data = {'price':'12'}
    data={'username':'test', 'password':'1'}
    auth=('test', '1')
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    
    r = requests.post(url, headers=headers, data=json.dumps(data))
    #r = requests.post('http://127.0.0.1:8000/play/login/?username=fraferra&password=1')
    print r.content    


if method=='home':
    #url = 'http://127.0.0.1:8000/play/home/'
    url = 'http://127.0.0.1:8000/play/home/?username=test&password=1'
    data={'password': '1', 'username':'test'}
    auth=('test', '1')
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    
    r = requests.get(url)#, auth=auth, data=data )
    print r.content  

if method=='leaderboard':
    url = 'http://127.0.0.1:8000/play/leaderboard/'
    data={'username':'test', 'password':'1'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} 
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print r.content    

if method=='coupons':
    url = 'http://127.0.0.1:8000/play/coupons/'
    data={'username':'test', 'password':'1'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} 
    r = requests.get(url, headers=headers, data=json.dumps(data))
    #r = requests.get(url+'?id_coupon=1', headers=headers, data=json.dumps(data))
    print r.content    

if method=='my_coupons':
    url = 'http://127.0.0.1:8000/play/my_coupons/'
    data={'username':'test', 'password':'1'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} 
    r = requests.get(url, headers=headers, data=json.dumps(data))
    #r = requests.get(url+'?id_coupon=1', headers=headers, data=json.dumps(data))
    print r.content  