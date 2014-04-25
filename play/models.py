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


class Player(models.Model):
    user=models.ForeignKey(User)
    custom_auth = forms.BooleanField(initial=False)
    token=models.CharField(max_length=100, null=True, default=None)
    score=models.DecimalField(max_digits=4, decimal_places=0, null=True, default=0)
    experience=models.DecimalField(max_digits=5, decimal_places=0, null=True, default=0)
    level=models.DecimalField(max_digits=4, decimal_places=0, null=True, default=0)
    picture_url=models.CharField(max_length=200, null=True, default=None)
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
    shop=models.ForeignKey(Shop)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.title) or u'' 

class Event(models.Model):
    title=models.CharField(max_length=100, null=True)
    description=models.TextField(max_length=500, null=True)
    location=models.CharField(max_length=100, null=True)
    experience=models.DecimalField(max_digits=5, decimal_places=0, null=True, default=0)
    #position = GeopositionField()
    points=models.DecimalField(max_digits=4, decimal_places=0)  
    participants = models.ManyToManyField(Player, default=None, null=True)
    event_type=models.CharField(max_length=50,choices=constants.TYPE, default=None)
    date=models.DateTimeField( null=True)
    organizer=models.ForeignKey(Organization)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.title) or u'' 

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