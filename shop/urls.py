from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from shop import views

urlpatterns = patterns('',

    url(r'^create_coupon/$', views.create_coupon ,name='create_coupon'),

    url(r'^my_coupons/$', views.my_coupons ,name='my_coupons'),

    url(r'^erase/$', views.erase ,name='erase'),

)

