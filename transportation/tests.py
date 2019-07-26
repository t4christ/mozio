import json
from account.models import User
from .models import Polygon
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.contrib.gis.geos import fromstr




class CreatePolygonAPIViewTestCase(APITestCase):
    url = reverse("transportation:create_polygon")

    def setUp(self):
        self.username = "temitayo"
        self.email = "temitayo@bakare.com"
        self.password = "password"
        self.name ="Temitayo Polygon"
        self.price="70000"
        self.lon="-19.456678"
        self.lat="36.456678"
        self.user = User.objects.create_user(self.username, self.email,self.password)
        self.api_authentication()

    def api_authentication(self):
           self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.token)

    def test_create_polygon(self):
        polygon_data ={
            "name":self.name,
            "price":self.price,
            "lon":self.lon,
            "lat":self.lat,
            "provider":self.user.pk
        }
        response = self.client.post(self.url, polygon_data,format='json')
        self.assertEqual(201, response.status_code)



class GetPolygonAPIViewTestCase(APITestCase):
    url = reverse("transportation:get_polygons")

    def test_getall_polygons(self):
        response = self.client.get(self.url,format='json')
        self.assertEqual(200, response.status_code)

    


class PolygonUpdateDeleteAPIViewTestCase(APITestCase):
    def setUp(self):
        self.username = "temitayo"
        self.email = "temitayo@bakare.com"
        self.password = "password"
        self.name ="Temitayo Polygon"
        self.price="80000"
        self.lon="-19.456678"
        self.lat="36.456678"
        self.cordinates = fromstr(f"POINT({self.lon} {self.lat})", srid=4326)
        self.user = User.objects.create_user(self.username, self.email,self.password)
        self.polygon = Polygon.objects.create(name=self.name, price=self.price,
                        location=self.cordinates,provider=self.user)
        self.api_authentication()

    def api_authentication(self):
           self.client.credentials(HTTP_AUTHORIZATION='token ' + self.user.token)
     
    
    def test_update_user(self):
        self.url = reverse("transportation:update_polygon",kwargs={'pk':self.polygon.pk})
        response = self.client.patch(self.url,{"name":"Temi Polygon",
                                    "price":"100000"},format='json')
        response_data = json.loads(response.content)
        self.assertEqual(200, response.status_code)


    def test_delete_user(self):
            self.url = reverse("transportation:delete_polygon",kwargs={'pk':self.polygon.pk})
            response = self.client.delete(self.url)
            self.assertEqual(204, response.status_code)