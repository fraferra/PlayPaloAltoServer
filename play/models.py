from django.db import models
from datetime import date
from django import forms
from django.contrib.auth.models import User,UserManager
from django.utils import timezone
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from utils import *
from social_auth.models import UserSocialAuth

# Create your models here.
class Coupon(models.Model):
	title=models.CharField(max_length=50, null=True)
	description=models.TextField(max_length=500, null=True)
	location=models.CharField(max_length=100, null=True)
	price=models.DecimalField(max_digits=4, decimal_places=0)



class Challenge(models.Model):
	title=models.CharField(max_length=50, null=True)
	description=models.TextField(max_length=500, null=True)
	location=models.CharField(max_length=100, null=True)
	points=models.DecimalField(max_digits=4, decimal_places=0)	

class CustomUser(models.Model):
    score=models.DecimalField(max_digits=4, decimal_places=0, null=True, default=None)
    user=models.ForeignKey(UserSocialAuth)	
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.score) or u''
#class Player(UserProfile):
#    user=models.ForeignKey(User, related_name="player")

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        #picture_url=pictureUrl(instance.get_profile().extra_data['access_token'])
        CustomUser.objects.create()


post_save.connect(create_user_profile, sender=UserSocialAuth)