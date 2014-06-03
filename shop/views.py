# Create your views here.
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
#from django.contrib.auth import authenticate, login as auth_login
from social_auth.models import UserSocialAuth
from play.models import *
from charity.models import *
from shop.models import *
from play.utils import *
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.models import User
import json
from django.contrib.auth import logout as django_logout
from shop.forms import *
from django.core.exceptions import *
from datetime import datetime



def create_coupon(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user

        try:
            #organization=Organization.objects.get(user=user)
            organization, shop=getShop(user)
            if request.method=='POST':
                form = CouponForm(request.POST) 
                if form.is_valid():
                    new_coupon = form.save(commit=False)
                    new_coupon.shop=shop
                    new_coupon.save()
                    return HttpResponseRedirect('/my_coupons/')
            else:
                form = CouponForm()
            return render(request, 'shop/create_coupon.html', {'form':form, 'shop':shop})
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/sorry/')

          

def my_coupons(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        organization, shop=getShop(user)
        if not organization:
            return HttpResponseRedirect('/sorry/')
        list_of_coupons=Coupon.objects.filter(shop=shop)
        number=len(list_of_coupons)
        id_delete=request.GET.get('delete','')
        if len(id_delete)!=0:
            coupon=Coupon.objects.get(pk=id_delete)
            coupon.delete()
            return HttpResponseRedirect('/my_coupons/')
        return render(request, 'shop/my_coupons.html', {'list_of_coupons':list_of_coupons, 'number':number, 'shop':shop})


def erase(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user=request.user
        organization, shop=getShop(user)
        if request.method == 'GET':
            id_user=request.GET['id_user']
            id_coupon=request.GET['id_coupon']
            coupon=Coupon.objects.get(id=id_coupon)
            player=Player.objects.get(id=id_user)
            player.coupon_set.remove(coupon)
            CouponHistory.objects.create(
                player=player,
                shop=shop.title,
                title=coupon.title,
                #coupon=coupon
                )
            player.save()
            coupon.save()
            return HttpResponseRedirect('/my_coupons/')





