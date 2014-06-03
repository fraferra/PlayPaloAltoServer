from django.contrib import admin
from charity.models import *
from django.contrib.auth.models import User


class OrganizationAdmin(admin.ModelAdmin):
	model=Organization
	fields=['title', 'location','user']



class EventAdmin(admin.ModelAdmin):
	model=Event
	fields=['title', 'description', 'location', 'participants', 'points', 'experience']




admin.site.register(Event, EventAdmin)
admin.site.register(Organization, OrganizationAdmin)