from django.contrib import admin
from play.models import *
from django.contrib.auth.models import User


class PlayerAdmin(admin.ModelAdmin):
	model=Player
	fields=['score', 'user']

class OrganizationAdmin(admin.ModelAdmin):
	model=Organization
	fields=['title', 'location','user']

class CouponAdmin(admin.ModelAdmin):
	model=Coupon
	fields=['title', 'description', 'location', 'buyers', 'price']

admin.site.register(Player, PlayerAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Organization, OrganizationAdmin)