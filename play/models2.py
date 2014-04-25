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

class CouponHistory(models.Model):
    title=models.CharField(max_length=100, null=True)
    #coupon=models.ForeignKey(Coupon, related_name='coupon')

    player=models.ForeignKey(Player, related_name ='participant')
    shop=models.ForeignKey(Shop, related_name='created')


class EventHistory(models.Model):
    date=models.DateTimeField( null=True)
    title=models.CharField(max_length=100, null=True)
    #event_done=models.ForeignKey(Event, related_name='created')
    
    player=models.ForeignKey(Player, related_name ='participant')
    points=models.DecimalField(max_digits=4, decimal_places=0) 
    organization=models.ForeignKey(Organization, related_name='organization')