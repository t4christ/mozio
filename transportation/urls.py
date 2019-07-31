from django.urls import path
from django.contrib.auth import views as auth_views



from .views import \
(
HomeAPIView,
RetrieveDestroyPolygonAPIView,
PolygonUpdateAPIView,
PolygonAPIView
)

app_name='transportation'

urlpatterns = [
    path('', HomeAPIView.as_view(),name="home"),
    path('create_polygon', RetrieveDestroyPolygonAPIView.as_view(),name="create_polygon"),
    path('get_polygons', PolygonAPIView.as_view(),name='get_polygons'),
    path('update_polygon/<int:id>', PolygonUpdateAPIView.as_view(), name ='update_polygon'),
    path('delete_polygon/<int:pk>', RetrieveDestroyPolygonAPIView.as_view(), name='delete_polygon')
]
 
    