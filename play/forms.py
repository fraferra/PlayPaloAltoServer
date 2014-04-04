from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
import string
from play.models import *
import constants

class EventForm(ModelForm):
    title=forms.CharField(widget = forms.TextInput(attrs={'style':'color:black'}))
    location=forms.CharField(widget = forms.TextInput(attrs={'style':'color:black'}))
    description=forms.CharField(widget = forms.Textarea(attrs={'style':'color:black'}))
    points=forms.DecimalField(widget = forms.TextInput(attrs={'style':'color:black;', 'size':'4'}))
    class Meta:
        model=Event
        fields = ('title','description','location','points','event_type', 'date')

class SignUpForm(UserCreationForm):
    """ Require email address when a user signs up """
    email = forms.EmailField(label='Email address', max_length=75)

    def __init__(self, *args, **kwargs): 
        super(SignUpForm, self).__init__(*args, **kwargs) 
        # remove username
        self.fields.pop('username')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name') 
        exclude=['username']

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError("This email address already exists. Did you forget your password?")
        except User.DoesNotExist:
            return email
        
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.username=user.email

        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.is_active = True # change to false if using email activation
        if commit:
            user.save()

        return user