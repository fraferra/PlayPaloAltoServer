from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from charity import views

urlpatterns = patterns('',
    
    url(r'^organization_home/$', views.organization_home ,name='organization_home'),
    url(r'^create_event/$', views.create_event ,name='create_event'),
    url(r'^my_events/$', views.my_events ,name='my_events'),

    url(r'^company/$', views.my_company ,name='my_company'),
    url(r'^reward/$', views.reward ,name='reward'),
)

