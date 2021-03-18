from django.contrib import admin
from django.urls import path


from plants.views import plant_create_view, plant_delete_view, PlantListView, plant_update_view 
#PlantUpdateView


urlpatterns = [
    
   
    #path ('create/', plant_create_view),
 
    path('<int:pk>/update/', plant_update_view, name= 'update-plant'),
    path('<int:pk>/delete/', plant_delete_view, name= 'delete-plant'),
    #path('<int:pk>/update/', PlantUpdateView.as_view(), name= 'update-plant'),
    
	path('', PlantListView.as_view(), name= 'plants'),
	path('create/', plant_create_view, name= 'create-plant' )
	]