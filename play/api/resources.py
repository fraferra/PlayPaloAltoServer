from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import (
Authentication, ApiKeyAuthentication, BasicAuthentication,
MultiAuthentication)
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie import fields
from django.db import IntegrityError
from play.models import *
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

class CreateUserResource(ModelResource):
    class Meta:
        allowed_methods = ['post']
        queryset=User.objects.all()
        object_class = User
        resource_name = 'newuser'
        authentication = Authentication()
        authorization = Authorization()
        include_resource_uri = False
        fields = ['username','first_name', 'email']
    def obj_create(self, bundle, request=None, **kwargs):
        try:
            bundle = super(CreateUserResource, self).obj_create(bundle)
            bundle.obj.set_password(bundle.data.get('password'))
            bundle.obj.save() 
        except IntegrityError:
            raise BadRequest('That username already exists')
        return bundle


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']

class PlayerResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Player.objects.all()
        resource_name = 'player'
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
        }


class CouponResource(ModelResource):
    buyers=fields.ToManyField(PlayerResource, 'buyers',full=True)
    class Meta:
        queryset = Coupon.objects.all()
        resource_name = 'coupon'
        authorization = Authorization()
        allowed_methods = ['post', 'get','put']

class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'
        allowed_methods = ['post', 'get']

class ChallengeResource(ModelResource):
    class Meta:
        queryset = Challenge.objects.all()
        resource_name = 'challenge'
        allowed_methods = ['post', 'get']