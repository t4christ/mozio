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
from rest_framework.generics import ListAPIView,RetrieveDestroyAPIView,RetrieveUpdateAPIView
from django.contrib.gis.geos import fromstr
from .models import Polygon
from account.models import User


from .serializers import (PolygonSerializer,RetrievePolygonSerializer)

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class PolygonAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RetrievePolygonSerializer
    def get_queryset(self):

                polygons = Polygon.objects.all()
                polygon_lon = self.request.query_params.get('lon', None)
                polygon_lat = self.request.query_params.get('lat', None)

                if polygon_lon and polygon_lat is not None:
                        cordinates = fromstr(f"POINT({polygon_lon} {polygon_lat})", srid=4326)
                        queryset = polygons.objects.filter(location=cordinates)
                        return queryset
                else:   

                        return polygons
    
        


class RetrieveDestroyPolygonAPIView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PolygonSerializer
    def post(self, request):
        if request.data["lon"] and request.data["lat"]:
            cordinates = fromstr(f"POINT({request.data['lon']} {request.data['lat']})", srid=4326)
            request.data['location'] = cordinates
            request.data['provider'] = request.user.pk
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        
    
        else:
            return Response({"message": "Longitude and Latitude is required."},status=204)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


 
    
    def delete(self, request, pk, format=None):
        delete_polygon = get_object_or_404(Polygon,provider=request.user,pk=pk)
        delete_polygon.delete()
        return Response({"message": "Your polygon has been deleted.".format(pk)},status=204)


class PolygonUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Polygon.objects.all()
    serializer_class = PolygonSerializer
    lookup_field = 'id'
    
    def perform_update(self, serializer):
        if self.request.data["lon"] and self.request.data["lat"]:
            cordinates = fromstr(f"POINT({self.request.data['lon']} {self.request.data['lat']})", srid=4326)
            self.request.data['location'] = cordinates
            serializer.save(provider=self.request.user,location=self.request.data['location'])
        serializer.save(provider=self.request.user)