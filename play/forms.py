from django.contrib.auth.models import User
from django.forms import ModelForm,Textarea
from django import forms
from django.contrib.auth.forms import UserCreationForm
import string
from play.models import *
import constants
import datetime

class IdeaForm(ModelForm):
    title=forms.CharField()
    description=forms.CharField(widget = forms.Textarea(attrs={}))
    points=forms.DecimalField(widget = forms.TextInput(attrs={ 'size':'4'}))
    experience=forms.DecimalField(widget = forms.TextInput(attrs={ 'size':'4'}))
    class Meta:
        model=Idea
        fields = ('title','description','author','points', 'experience')

class CommentForm(ModelForm):
    comment=forms.CharField(widget = forms.Textarea) 
    class Meta:
        model=Comment
        fields = ('comment',)
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['comment'].widget.attrs['cols'] = 15
        self.fields['comment'].widget.attrs['rows'] = 1


class CommentFeedForm(ModelForm):
    comment=forms.CharField(widget = forms.Textarea) 
    class Meta:
        model=CommentFeed
        fields = ('comment', )
    def __init__(self, *args, **kwargs):
        super(CommentFeedForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['comment'].widget.attrs['cols'] = 15
        self.fields['comment'].widget.attrs['rows'] = 1


class EditUserForm(ModelForm):
    class Meta:
        model=User
        fields = ('username',)

class EditPicForm(ModelForm):
    class Meta:
        model=Player
        fields = ('picture_url', 'facebook_pic')

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