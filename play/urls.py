from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from play import views

urlpatterns = patterns('',
    url(r'^login/$', views.login ,name='login'),
    url(r'^$', views.home ,name='home'),
    url(r'^coupons/$', views.coupons ,name='coupons'),
    url(r'^my_coupons/$', views.my_coupons ,name='my_coupons'),
    url(r'^leaderboard/$', views.leaderboard ,name='leaderboard'),

)

