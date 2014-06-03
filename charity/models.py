from django.db import models
from datetime import date
from django import forms
from django.contrib.auth.models import User,UserManager
from django.utils import timezone
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from play.utils import *
from social_auth.models import UserSocialAuth
from play import constants
from django.core.exceptions import *
import play.models
import shop.models
# Create your models here.
import requests
import datetime


class Organization(models.Model):
    user=models.ForeignKey(User)
    title=models.CharField(max_length=100, null=True, default='Super Duper!')
    location=models.CharField(max_length=100, null=True)
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
    participants = models.ManyToManyField('play.Player', default=None, null=True)
    event_type=models.CharField(max_length=50,choices=constants.TYPE, default=None)
    date=models.DateTimeField( null=True, default=None)
    organizer=models.ForeignKey(Organization)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.title) or u'' 

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


