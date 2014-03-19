import requests

token ='CAAESosN1MxkBAFKixjZCpI99uE3MGCQgjQ5UySJWS4vTxDfEstDJoVZAg8quOhX3jHs9A5u2W1yMTfzzfFxMVMRfeNHWQMfPAuDn9xjGJGrsOBHrKRePJhSVgKd4AmdHiJ6SZAwe9dS7mjtZC4JNawWxociBL2vpigvu7dQprZC0mj6DLNBaQxXCWIZAcQrk0ZD'


r=requests.get('https://graph.facebook.com',
	           params={'token':token, 'fields':'id,name,picture'})

print r.json()

url = 'https://graph.facebook.com/me/?fields=id,name,picture&access_token='+token
rr=requests.get(url).json()['picture']['data']['url']
print rr