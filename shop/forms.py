from django.contrib.auth.models import User
from django.forms import ModelForm,Textarea
from django import forms
from django.contrib.auth.forms import UserCreationForm
import string
from shop.models import *
import play.constants
import datetime



class CouponForm(ModelForm):
    title=forms.CharField()
    location=forms.CharField(widget = forms.TextInput(attrs={ 'size':'30'}))
    description=forms.CharField(widget = forms.Textarea(attrs={}))
    price=forms.DecimalField(widget = forms.TextInput(attrs={ 'size':'4'}))
    coupons_released=forms.DecimalField(widget = forms.TextInput(attrs={ 'size':'4'}))
    class Meta:
        model=Coupon
        fields = ('title','description','location','price','coupons_released')
