from django.contrib.auth.models import User
from rest_framework import serializers
from core.models import Village, Region, ArmyRequest


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name')


class RegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')


class VillageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Village
        fields = ('id', 'name', 'region', 'x', 'y',)

class ArmyRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    village = VillageSerializer()
    class Meta:
        model = ArmyRequest
        fields = ('user', 'village', 'type')
