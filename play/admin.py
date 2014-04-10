from django.contrib import admin
from play.models import *
from django.contrib.auth.models import User


class PlayerAdmin(admin.ModelAdmin):
	model=Player
	fields=['score', 'user', 'picture_url']

class OrganizationAdmin(admin.ModelAdmin):
	model=Organization
	fields=['title', 'location','user']

class CouponAdmin(admin.ModelAdmin):
	model=Coupon
	fields=['title', 'description', 'location', 'buyers', 'price']

class EventAdmin(admin.ModelAdmin):
	model=Event
	fields=['title', 'description', 'location', 'participants', 'points', 'experience']



admin.site.register(Player, PlayerAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Organization, OrganizationAdmin)