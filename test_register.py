import requests
import json
from urllib2 import urlopen
import datetime
import simplejson

url = 'http://127.0.0.1:8000/api/v1/newuser/'
data = {'username' :'s3@gmail.com', 'password' : 'newpass'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
print json.dumps(data)
r = requests.post(url, data=json.dumps(data), headers=headers)
print r.content