from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from play import views

urlpatterns = patterns('',
    url(r'^login/$', views.login ,name='login'),  
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^home/$', views.home ,name='home'),
    url(r'^sorry/$', views.sorry ,name='sorry'),
    url(r'^create/$', views.create_event ,name='create_event'),
    url(r'^my_events/$', views.my_events ,name='my_events'),
    url(r'^company/$', views.my_company ,name='my_company'),
    url(r'^reward/$', views.reward ,name='reward'),
    url(r'^$', views.index ,name='index'),




    url(r'^api_registration/$', views.api_registration ,name='api_registration'),
    url(r'^api_login/$', views.api_login ,name='api_login'),
    url(r'^coupons/$', views.coupons ,name='coupons'),
    url(r'^api_my_events/$', views.api_my_events ,name='api_my_events'),
    url(r'^leaderboard/$', views.leaderboard ,name='leaderboard'),

)

