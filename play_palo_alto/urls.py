from django.conf.urls import patterns, include, url
from tastypie.api import Api
from play.api.resources import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(PlayerResource())
v1_api.register(EventResource())
v1_api.register(CouponResource())
v1_api.register(ChallengeResource())
v1_api.register(CreateUserResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^play_palo_alto/', include('play_palo_alto.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^play/', include('play.urls', namespace="play")),
    url(r'', include('social_auth.urls')),
    (r'^api/', include(v1_api.urls)),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
)
