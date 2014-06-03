from django.db import models
from datetime import date
from django import forms
from django.contrib.auth.models import User,UserManager
from django.utils import timezone
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from play.utils import *
from social_auth.models import UserSocialAuth
import play.constants
from django.core.exceptions import *
import charity.models
import play.models
# Create your models here.
import requests
import datetime
# Create your models here.


class Shop(models.Model):
    user=models.ForeignKey(User)
    title=models.CharField(max_length=100, null=True, default='Super shop!')
    location=models.CharField(max_length=100, null=True)
    picture_url=models.CharField(max_length=200, null=True, default='/static/img/stanford.png')
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.title) or u''   


class Coupon(models.Model):
    title=models.CharField(max_length=50, null=True)
    description=models.TextField(max_length=500, null=True)
    location=models.CharField(max_length=100, null=True)
    price=models.DecimalField(max_digits=4, decimal_places=0)
    buyers=models.ManyToManyField('play.Player', default=None, null=True)
    picture_url=models.CharField(max_length=200, null=True, default='/static/img/stanford.png')
    shop=models.ForeignKey(Shop)
    coupons_released=models.DecimalField(max_digits=4, decimal_places=0, default=10)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.title) or u'' 

def assign_coupon_pic(sender, instance, created, **kwargs):
    if created:
        instance.picture_url=instance.shop.picture_url
        instance.save()
post_save.connect(assign_coupon_pic, sender=Coupon)