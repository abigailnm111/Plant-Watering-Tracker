from django.contrib import admin
from django.urls import path


from plants.views import    PlantListView,  plant_create_view, PlantUpdateView, PlantDeleteView


urlpatterns = [
    
   
    #path ('create/', plant_create_view),
 
    path('<int:pk>/update/', PlantUpdateView.as_view(), name= 'update-plant'),
    path('<int:pk>/delete/', PlantDeleteView.as_view(), name= 'delete-plant'),
    
	path('', PlantListView.as_view(), name= 'plants'),
	path('create/', plant_create_view, name= 'create-plant' )
	]