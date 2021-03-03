from django.contrib import admin
from django.urls import path

from pages.views import home_view 
from plants.views import plant_create_view, plant_update_view, plant_list_view, dynamic_lookup_view, plant_delete_view

urlpatterns = [
    
    path('', plant_list_view, name='plants' ),
    path ('create/', plant_create_view),
   
    path('update/<int:id>/update/', plant_update_view),
    path('/<int:id>/delete/', plant_delete_view),
    path('/<int:id>/', dynamic_lookup_view, name= 'dynamic')
]