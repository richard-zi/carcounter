from django.contrib import admin
from django.urls import path
from api_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/save_vehicle_data/', views.save_vehicle_data, name='save_vehicle_data'),
    path('api/get_all_vehicle_data/', views.get_all_vehicle_data, name='get_all_vehicle_data'),

]
