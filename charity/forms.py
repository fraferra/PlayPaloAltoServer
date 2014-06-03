from django.contrib.auth.models import User
from django.forms import ModelForm,Textarea
from django import forms
from django.contrib.auth.forms import UserCreationForm
import string
from charity.models import *
import play.constants
import datetime

class CompanyForm(ModelForm):
    class Meta:
        model=Organization
        fields=('title', 'location')



class EventForm(ModelForm):
    title=forms.CharField()
    location=forms.CharField(widget = forms.TextInput(attrs={ 'size':'30'}))
    description=forms.CharField(widget = forms.Textarea(attrs={}))
    points=forms.DecimalField(widget = forms.TextInput(attrs={ 'size':'4'}))
    experience=forms.DecimalField(widget = forms.TextInput(attrs={ 'size':'4'}))
    date = forms.DateTimeField(initial=datetime.datetime.now)
    class Meta:
        model=Event
        fields = ('title','description','location','points','event_type', 'date', 'experience', 'challenge_event')
