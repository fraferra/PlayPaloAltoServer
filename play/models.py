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
import charity.models
import shop.models
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
    event_type=models.CharField(max_length=50,choices=constants.TYPE, default=None, null=True)
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
    event=models.ForeignKey('charity.Event')
    date=models.DateTimeField( null=True, default=datetime.datetime.now)


class Feed(models.Model):
    player=models.ForeignKey(Player)
    event=models.ForeignKey('charity.Event')
    likes= models.DecimalField(max_digits=4, decimal_places=0, default=0)
    date=models.DateTimeField( null=True, default=datetime.datetime.now)
 


class CommentFeed(models.Model):
    comment=models.TextField(max_length=500, null=True)
    commenter=models.ForeignKey(Player)
    feed=models.ForeignKey(Feed)
    date=models.DateTimeField( null=True, default=datetime.datetime.now)



class Badge(models.Model):
    player=models.ForeignKey(Player)
    title=models.CharField(max_length=100, null=True, default='Beginner!')
    icon=models.CharField(max_length=50,choices=constants.ICON, default='fa-thumbs-o-up')

'''
def assign_badge(sender, instance, created, **kwargs):
    if created:
        badge=Badge.objects.create(player=instance.player)
        type_event=['Animals', 'Food','Art', 'Shopping', 'Elders', 'Environment']
        for tt in type_event:



        
post_save.connect(assign_badge, sender=EventHistory) '''