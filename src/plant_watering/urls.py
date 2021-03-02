"""plant_watering URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from pages.views import home_view 
from plants.views import plant_create_view, plant_update_view, plant_list_view, dynamic_lookup_view, plant_delete_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('plants/', plant_list_view, name='plants' ),
    path ('create/', plant_create_view),
   
    path('update/<int:id>/update/', plant_update_view),
    path('plants/<int:id>/delete/', plant_delete_view),
    path('plants/<int:id>/', dynamic_lookup_view, name= 'dynamic')
]
