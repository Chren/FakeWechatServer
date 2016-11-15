from rest_framework import serializers
from relationship.models import IMUser, FriendShip
from django.contrib.auth.models import User
from rest_framework.fields import Field

class IMUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IMUser
        fields = ('userid', 'phone', 'name',
                  'photo', 'bgimg')

class LoginUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IMUser
        fields = ('userid', 'phone', 'name',
                  'photo', 'bgimg', 'token', 'rctoken')

class ResponseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IMUser
        fields = ('userid', 'phone', 'name',
                  'photo', 'bgimg', 'token', 'rctoken')