import requests
from bs4 import BeautifulSoup
import re

'''
def returnPaloAltoEvent():
    url='http://www.yelp.com/events/palo-alto'
    event_page=BeautifulSoup(requests.get(url).text)
    popular_events_div = event_page.find(id="popular_events")
    events_yelp=re.findall('<span itemprop="name">([\w.-]+)</span>')
    return events_yelp

'''
'''
url='http://www.yelp.com/events/palo-alto'
event_page=BeautifulSoup(requests.get(url).text)
test2=[]
popular_events_div = event_page.find(id="popular_events")
test = event_page.find_all('h3')
for t in test:
    t2= t.find('a')
    if not t2 is None:
        print t2
        #print t2.find('span').text
    test2.append((t.find('a')))'''

#events_yelp=re.findall('<img class="photo-box-img" alt="([.]+)"', str(popular_events_div))
#events_yelp=re.findall('<a href=" ', str(popular_events_div))
#events_yelp=re.findall('<span itemprop="name">([\w\.\s\b\d\&\@]+)', str(popular_events_div))
#events_yelp=re.findall('<span itemprop="name">([.]+)', str(popular_events_div))
#events_yelp=re.findall('src="http://s3-media2.ak.yelpcdn.com/ephoto/([\w\d\.\-]+)/ms.jpg"', str(popular_events_div))
#print popular_events_div
#print test2, len(test2)
  
url='http://www.yelp.com/events/palo-alto'
event_page=BeautifulSoup(requests.get(url).text)
links=[]
popular_events_div = event_page.find(id="popular_events")
liks_h3 = event_page.find_all('h3')
for t in liks_h3:
    t2= t.find('a')
    if not t2 is None:
        #print t2
        print t2['href']
        
        print t2.find('span').text
        links.append((t.find('a')))
print links



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
