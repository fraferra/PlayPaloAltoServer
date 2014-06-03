from django.contrib import admin
from play.models import *
from django.contrib.auth.models import User


class PlayerAdmin(admin.ModelAdmin):
	model=Player
	fields=['score', 'user', 'picture_url', 'experience']



class IdeaAdmin(admin.ModelAdmin):
	model=Idea
	fields=['title', 'description', 'points', 'experience', 'author'] 


admin.site.register(Idea, IdeaAdmin) 
admin.site.register(Player, PlayerAdmin)
