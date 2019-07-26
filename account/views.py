from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.core import serializers
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import User


from .serializers import (RegistrationSerializer,LoginSerializer,UserSerializer)

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    def post(self, request):
        password = request.data.get('password', {})
        email = request.data.get('email', {})
        confirm_password=request.data.get('confirm_password',{})
        if password == confirm_password:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(email=email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return  Response('Passwords must match')

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        
        if(request.user.is_superuser):
            if 'provider' in cache:
                # get results from cache
                providers = cache.get('provider')
                return Response(providers, status=status.HTTP_201_CREATED)
 
            else:
                providers = User.objects.all()
                serialized_provider = serialized_obj = serializers.serialize('python', providers)
                results = [provider for provider in serialized_provider]
                # store data in cache
                cache.set("provider",results, timeout=CACHE_TTL)
                return Response(results, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = {
            'username': request.data.get('username', request.user.username),
            'name': request.data.get('name', request.user.name),
            'phone_number': request.data.get('phone_number', request.user.phone_number),
            'email': request.data.get('email', request.user.email),
            'language': request.data.get('language', request.user.language),
            'currency': request.data.get('currency', request.user.currency),
        }
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        delete_user = get_object_or_404(User, pk=pk)
        delete_user.delete()
        return Response({"message": "Your account has been deleted.".format(pk)},status=204)

        



