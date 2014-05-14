from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from play import views, api

urlpatterns = patterns('',
    url(r'^login/$', views.login ,name='login'),  
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^organization_home/$', views.organization_home ,name='organization_home'),
    url(r'^idea/$', views.idea ,name='idea'),
    url(r'^sorry/$', views.sorry ,name='sorry'),
    url(r'^create_event/$', views.create_event ,name='create_event'),
    url(r'^create_coupon/$', views.create_coupon ,name='create_coupon'),
    url(r'^my_events/$', views.my_events ,name='my_events'),
    url(r'^my_coupons/$', views.my_coupons ,name='my_coupons'),
    url(r'^company/$', views.my_company ,name='my_company'),
    url(r'^reward/$', views.reward ,name='reward'),
    url(r'^erase/$', views.erase ,name='erase'),
    url(r'^$', views.index ,name='index'),
    url(r'^event/$', views.event ,name='event'),
    url(r'^home/$', views.home ,name='home'),
    url(r'^look_events/$', views.look_events ,name='look_events'),
    url(r'^look_coupons/$', views.look_coupons ,name='look_coupons'),
    url(r'^leaderboard/$', views.leaderboard ,name='leaderboard'),
    url(r'^feeds/$', views.feeds ,name='feeds'),
)

