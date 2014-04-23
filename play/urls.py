from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from play import views, api

urlpatterns = patterns('',
    url(r'^login/$', views.login ,name='login'),  
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^home/$', views.home ,name='home'),
    url(r'^sorry/$', views.sorry ,name='sorry'),
    url(r'^create_event/$', views.create_event ,name='create_event'),
    url(r'^create_coupon/$', views.create_coupon ,name='create_coupon'),
    url(r'^my_events/$', views.my_events ,name='my_events'),
    url(r'^my_coupons/$', views.my_coupons ,name='my_coupons'),
    url(r'^company/$', views.my_company ,name='my_company'),
    url(r'^reward/$', views.reward ,name='reward'),
    url(r'^erase/$', views.erase ,name='erase'),
    url(r'^$', views.index ,name='index'),




    url(r'^api/registration/$', views.api_registration ,name='api_registration'),

    url(r'^api/v1/login/$', views.api_v1_login ,name='api_login'),
    url(r'^api/v1/home/$', views.api_v1_home ,name='api_home'),
    url(r'^api/v1/logout/$', views.api_v1_logout ,name='api_logout'),
    url(r'^api/v1/my_events/$', views.api_v1_my_events ,name='api_my_events'),
    url(r'^api/v1/events/$', views.api_v1_events ,name='api_events'),
    url(r'^api/v1/my_coupons/$', views.api_v1_my_coupons ,name='api_my_coupons'),
    url(r'^api/v1/coupons/$', views.api_v1_coupons ,name='api_coupons'),
    url(r'^api/v1/leaderboard/$', views.api_v1_leaderboard ,name='api_leaderboard'),


    url(r'^api/v2/login/$', views.api_v2_login ,name='api_login'),
    url(r'^api/v2/home/$', views.api_v2_home ,name='api_home'),
    url(r'^api/v2/logout/$', views.api_v2_logout ,name='api_logout'),
    url(r'^api/v2/my_events/$', views.api_v2_my_events ,name='api_my_events'),
    url(r'^api/v2/events/$', views.api_v2_events ,name='api_events'),
    url(r'^api/v2/my_coupons/$', views.api_v2_my_coupons ,name='api_my_coupons'),
    url(r'^api/v2/coupons/$', views.api_v2_coupons ,name='api_coupons'),
    url(r'^api/v2/leaderboard/$', views.api_v2_leaderboard ,name='api_leaderboard'),

)

