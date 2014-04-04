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
# Create your models here.

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        #UserProfile.objects.create(user=instance)
        Player.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)


class Player(models.Model):
    user=models.ForeignKey(User)
    score=models.DecimalField(max_digits=4, decimal_places=0, null=True, default=0)
    experience=models.DecimalField(max_digits=5, decimal_places=0, null=True, default=0)
    level=models.DecimalField(max_digits=4, decimal_places=0, null=True, default=0)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.user) or u'' 
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
'''
class CustomUser(models.Model):
    score=models.DecimalField(max_digits=4, decimal_places=0, null=True, default=0)
    experience=models.DecimalField(max_digits=5, decimal_places=0, null=True, default=0)
    #user=models.ForeignKey(UserSocialAuth)
    user=models.ForeignKey()
    facebook_id=models.DecimalField(max_digits=20, decimal_places=0)
    picture_url=models.CharField(max_length=200, null=True, default=None)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.score) or u''

#class Player(UserProfile):
#    user=models.ForeignKey(User, related_name="player")

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        facebook_id=instance.uid
        CustomUser.objects.create(user=instance, facebook_id=facebook_id)

post_save.connect(create_user_profile, sender=UserSocialAuth)
#post_save.connect(update_user_profile, sender=CustomUser)
'''

class Coupon(models.Model):
    title=models.CharField(max_length=50, null=True)
    description=models.TextField(max_length=500, null=True)
    location=models.CharField(max_length=100, null=True)
    price=models.DecimalField(max_digits=4, decimal_places=0)
    buyers=models.ManyToManyField(Player, default=None, null=True)
    #shop=models.ForeignKey(Shop)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.title) or u'' 
class Event(models.Model):
    title=models.CharField(max_length=50, null=True)
    description=models.TextField(max_length=500, null=True)
    location=models.CharField(max_length=100, null=True)
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