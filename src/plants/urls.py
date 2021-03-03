from django.contrib import admin
from django.urls import path


from plants.views import    PlantListView, PlantDetailView, PlantCreateView, PlantUpdateView, PlantDeleteView


urlpatterns = [
    
   
    #path ('create/', plant_create_view),
 
    path('<int:pk>/update/', PlantUpdateView.as_view(), name= 'update-plant'),
    path('<int:pk>/delete/', PlantDeleteView.as_view(), name= 'delete-plant'),
    
	path('', PlantListView.as_view(), name= 'plants'),
	path('<int:pk>/', PlantDetailView.as_view(), name= 'plant-detail'),
	path('create/', PlantCreateView.as_view(), name= 'create-plant' )
	]