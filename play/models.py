from django.db import models
from datetime import date
from django import forms
from django.contrib.auth.models import User,UserManager
from django.utils import timezone
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from utils import *
from social_auth.models import UserSocialAuth
import constants
from django.core.exceptions import *

# Create your models here.
import requests
import datetime
#from social_auth.backends.pipeline.user import update_user_details
class Player(models.Model):
    user=models.ForeignKey(User)
    custom_auth = forms.BooleanField(initial=False)
    token=models.CharField(max_length=100, null=True, default=None)
    score=models.DecimalField(max_digits=4, decimal_places=0, null=True, default=20)
    experience=models.DecimalField(max_digits=5, decimal_places=0, null=True, default=0)
    level=models.DecimalField(max_digits=4, decimal_places=0, null=True, default=0)
    picture_url=models.CharField(max_length=200, null=True, default='/static/img/avatar-1.png')
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.user) or u'' 


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        
post_save.connect(create_user_profile, sender=User)



'''
def create_pic(sender, instance, created, **kwargs):
    if created:
        #UserProfile.objects.create(user=instance)
        try:
            user=instance.user
            social=UserSocialAuth.objects.get(user=user)
            token=social.extra_data['access_token']
            url = 'https://graph.facebook.com/me/?fields=id,name,picture&access_token='+token
            rr=requests.get(url).json()['picture']['data']['url']
            instance.picture_url=rr
            instance.save()
        except ObjectDoesNotExist:
            pass

post_save.connect(create_pic, sender=Player)
'''

class Shop(models.Model):
    user=models.ForeignKey(User)
    title=models.CharField(max_length=100, null=True, default='Super shop!')
    location=models.CharField(max_length=100, null=True)
    picture_url=models.CharField(max_length=200, null=True, default='/static/img/stanford.png')
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.title) or u''   

class Organization(models.Model):
    user=models.ForeignKey(User)
    title=models.CharField(max_length=100, null=True, default='Super Duper!')
    location=models.CharField(max_length=100, null=True)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.title) or u''

class Coupon(models.Model):
    title=models.CharField(max_length=50, null=True)
    description=models.TextField(max_length=500, null=True)
    location=models.CharField(max_length=100, null=True)
    price=models.DecimalField(max_digits=4, decimal_places=0)
    buyers=models.ManyToManyField(Player, default=None, null=True)
    picture_url=models.CharField(max_length=200, null=True, default='/static/img/stanford.png')
    shop=models.ForeignKey(Shop)
    coupons_released=models.DecimalField(max_digits=4, decimal_places=0, default=10)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.title) or u'' 

class Event(models.Model):
    title=models.CharField(max_length=100, null=True)
    description=models.TextField(max_length=500, null=True)
    location=models.CharField(max_length=100, null=True)
    picture_url=models.CharField(max_length=200, null=True, default='/static/img/stanford.png')
    experience=models.DecimalField(max_digits=5, decimal_places=0, null=True, default=0)
    #position = GeopositionField()
    challenge_event=models.CharField(max_length=50,choices=constants.CHALLENGE_EVENT, default='Event')
    points=models.DecimalField(max_digits=4, decimal_places=0)  
    participants = models.ManyToManyField(Player, default=None, null=True)
    event_type=models.CharField(max_length=50,choices=constants.TYPE, default=None)
    date=models.DateTimeField( null=True, default=None)
    organizer=models.ForeignKey(Organization)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.title) or u'' 

def assign_coupon_pic(sender, instance, created, **kwargs):
    if created:
        instance.picture_url=instance.shop.picture_url
        instance.save()
post_save.connect(assign_coupon_pic, sender=Coupon)

def assign_event_pic(sender, instance, created, **kwargs):
    if created:
        if instance.event_type=='Animals':
            instance.picture_url='/static/img/animal.png'
        if instance.event_type=='Food':
            instance.picture_url='/static/img/food.png'
        if instance.event_type=='Elders':
            instance.picture_url='/static/img/elder.png'
        if instance.event_type=='Art':
            instance.picture_url='/static/img/art.png'
        if instance.event_type=='Environment':
            instance.picture_url='/static/img/environment.png'
        if instance.event_type=='Shopping':
            instance.picture_url='/static/img/shopping.png'
        instance.save()
post_save.connect(assign_event_pic, sender=Event)



class Challenge(models.Model):
    title=models.CharField(max_length=50, null=True)
    challenge_type=models.CharField(max_length=50,choices=constants.TYPE, default=None)
    description=models.TextField(max_length=500, null=True)
    location=models.CharField(max_length=100, null=True)
    points=models.DecimalField(max_digits=4, decimal_places=0)    
    participants = models.ManyToManyField(Player)


class CouponHistory(models.Model):
    title=models.CharField(max_length=100, null=True)
    #coupon=models.ForeignKey(Coupon, related_name='coupon')
    shop=models.CharField(max_length=100, null=True)
    player=models.ForeignKey(Player)
    #shop=models.ForeignKey(Shop, related_name='created')


class EventHistory(models.Model):
    date=models.DateTimeField( null=True)
    title=models.CharField(max_length=100, null=True)
    #event_done=models.ForeignKey(Event, related_name='created')
    organization=models.CharField(max_length=100, null=True)
    player=models.ForeignKey(Player)
    points=models.DecimalField(max_digits=4, decimal_places=0) 
    #organization=models.ForeignKey(Organization, related_name='organization')

class Idea(models.Model):
    title=models.CharField(max_length=100, null=True)
    author=models.CharField(max_length=100, null=True)
    description=models.TextField(max_length=500, null=True)
    points=models.DecimalField(max_digits=4, decimal_places=0)
    experience=models.DecimalField(max_digits=5, decimal_places=0, null=True, default=0) 



class Comment(models.Model):
    comment=models.TextField(max_length=500, null=True)
    commenter=models.ForeignKey(Player)
    event=models.ForeignKey(Event)
    date=models.DateTimeField( null=True, default=datetime.datetime.now)


class Feed(models.Model):
    player=models.ForeignKey(Player)
    event=models.ForeignKey(Event)
    likes= models.DecimalField(max_digits=4, decimal_places=0, default=0)
    date=models.DateTimeField( null=True, default=datetime.datetime.now)
 


class CommentFeed(models.Model):
    comment=models.TextField(max_length=500, null=True)
    commenter=models.ForeignKey(Player)
    feed=models.ForeignKey(Feed)
    date=models.DateTimeField( null=True, default=datetime.datetime.now)

