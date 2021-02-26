from django.http import HttpResponse
from django.shortcuts import render

from .forms import PlantForm
from .models import plants
# Create your views here.
def plant_create_view(request):
	form=PlantForm(request.POST or None)
	if form.is_valid():
		form.save()
		form= PlantForm()
	context = {
	'form':form
	}
	return render (request, "plants/plants_create.html",context)

def plant_detail_view(*args, **kwargs):
	return render (request, "home.html", {})

def plant_list_view(request):
	queryset=Plant.objects.all()
	context= {
		"object_list": queryset
	}
	return render (request,"plants/plant_list.html", context)