from django.contrib import admin
from shop.models import *
from django.contrib.auth.models import User

class ShopAdmin(admin.ModelAdmin):
	model=Shop
	fields=['title', 'location','user']


class CouponAdmin(admin.ModelAdmin):
	model=Coupon
	fields=['title', 'description', 'location', 'buyers', 'price']



admin.site.register(Shop, ShopAdmin)

admin.site.register(Coupon, CouponAdmin)
