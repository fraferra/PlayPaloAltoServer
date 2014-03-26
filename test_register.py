import requests
import json
from urllib2 import urlopen
import datetime
import simplejson
import sys
arg=sys.argv[1]
print arg
if arg=='user':
	url = 'http://127.0.0.1:8000/api/v1/newuser/'
	data = {'username' :'lol', 'password' : 'newpass', 'email':'test@ucl.com', 'first_name':'fra'}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	print json.dumps(data)
	r = requests.post(url, data=json.dumps(data), headers=headers)
	print r.content
if arg=='player':
	url = 'http://127.0.0.1:8000/api/v1/player/1/'
	data = {'score' :'12', 'user':'/api/v1/user/1/'}
	auth=('fraferra', '1')
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	print json.dumps(data)
	r = requests.put(url, data=json.dumps(data), headers=headers, auth=auth)
	print r.content	