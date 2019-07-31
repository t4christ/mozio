from rest_framework import serializers
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from account.serializers import UserSerializer
from account.models import User
from .models import Polygon




class PolygonSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    price = serializers.CharField(max_length=255)

    class Meta:
        model = Polygon
        fields = ('id','name', 'provider', 'price','location',)



class RetrievePolygonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Polygon
        fields = ('id','name', 'provider', 'price','location',)

    # def validate(self, data):
    #     name = data.get('name', None)
    #     provider = data.get('provider', None)
    #     provider = get_object_or_404(User,username=provider)
    #     price = data.get('price', None)
    #     location = data.get('location', None)
    #     print("location",data)
    #     # Raise an exception if a
    #     # price is not provided.
    #     if name is None:
    #         raise serializers.ValidationError(
    #             'A polygon name is required to create a polygon.'
    #         )

    #     # Raise an exception if a
    #     # price is not provided.
    #     if price is None:
    #         raise serializers.ValidationError(
    #             'A price is required to create a polygon.'
    #         )

    #     # Raise an exception if a
    #     # location is not provided.
    #     if location is None:
    #         raise serializers.ValidationError(
    #             'A location is required to create a polygon.'
    #         )


        
    #     location = Polygon.objects.create(name=name,provider=self.provider,price=price,location=location)

       
    #     return {
    #         'name': location.name,
    #         'provider': location.provider,
    #         'price': location.price,
    #         'location': location.location
    #     }


