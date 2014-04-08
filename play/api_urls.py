from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from play import views

urlpatterns = patterns('',
    url(r'^registration/$', views.api_registration ,name='api_registration'),
    url(r'^login/$', views.api_login ,name='api_login'),
    url(r'^logout/$', views.api_logout ,name='api_logout'),
    url(r'^my_events/$', views.api_my_events ,name='api_my_events'),
    url(r'^events/$', views.api_events ,name='api_events'),
    url(r'^my_coupons/$', views.api_my_coupons ,name='api_my_coupons'),
    url(r'^coupons/$', views.api_coupons ,name='api_coupons'),
    url(r'^leaderboard/$', views.api_leaderboard ,name='api_leaderboard'),

)

