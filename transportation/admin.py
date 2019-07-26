from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Polygon

@admin.register(Polygon)
class PolygonAdmin(OSMGeoAdmin):
    list_display = ('provider', 'location')