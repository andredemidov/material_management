from rest_framework import serializers
from .models import DeliveryQuery, ObjectType, Object, DeliveryQueryPosition, \
    Requirement, Contractor, MaterialType


class ObjectTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObjectType
        fields = ['__all__']

    # def create(self, validated_data):
    #     existed = ObjectType.objects.get(name=validated_data.get('name'))
    #     return existed if existed else ObjectType.objects.create(**validated_data)


class ObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Object
        fields = ['__all__']
        depth = 1


class DeliveryQuerySerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryQuery
        fields = ['__all__']
        depth = 1


class DeliveryQueryPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryQueryPosition
        fields = ['__all__']
        depth = 1


class RequirementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requirement
        fields = ['__all__']
        depth = 1


class ContractorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contractor
        fields = ['__all__']


class MaterialTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaterialType
        fields = ['id', 'name']
