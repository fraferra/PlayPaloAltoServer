from django.contrib import admin
from play.models import *
from django.contrib.auth.models import User


class UserProfileAdmin(admin.ModelAdmin):
	model=CustomUser
	fields=['score', 'user']


admin.site.register(CustomUser, UserProfileAdmin)
