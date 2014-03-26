from django.contrib import admin
from play.models import *
from django.contrib.auth.models import User


class PlayerAdmin(admin.ModelAdmin):
	model=Player
	fields=['score', 'user']


admin.site.register(Player, PlayerAdmin)
