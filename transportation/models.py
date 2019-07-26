from django.contrib.gis.db import models
from account.models import User,TimestampedModel

# Create a polygon class for geojson data with django gis database (POSTGIS)
class Polygon(TimestampedModel):
    provider = models.ForeignKey(User,on_delete=models.CASCADE,related_name='provider')
    name = models.CharField(default="",max_length=100)
    price= models.CharField(default="",max_length=100)
    location = models.PointField()


    def __str__(self):
        return f"{self.provider}'s Polygon"