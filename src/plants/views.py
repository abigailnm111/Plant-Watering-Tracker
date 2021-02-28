from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .forms import PlantForm
from .models import plants
# Create your views here.

# def plant_create_view(request):
# 	form= RawPlantForm()
# 	if request.method == "POST":
# 		form=RawPlantForm(request.POST)
# 		if form.is_valid():
# 			print(form.cleaned_data)
# 			plants.objects.create(**form.cleaned_data)
# 		else:
# 			print(form.errors)
# 	context= {
# 		"form": form
# 	}
# 	return render(request, "plants/plants_create.html", context)

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
	queryset=plants.objects.all()
	context= {
		"object_list": queryset
	}
	return render (request,"plants/plant_list.html", context)

def plant_update_view(request, id):
	obj= plants.objects.get(id=id)
	form=PlantForm(request.POST or none, instance=obj)
	if form.is_valid():
		form.save()
	context= {
	'form': form
	}
	return render(request, "plants/plant_update.html", context)

def plant_delete_view(request, id):
	obj= get_object_or_404(plants,id=id)
	if request.method== 'POST':
		obj.delete()

	context= {
		"object":obj
	}
	return render('plants/plant_delete.html', context)
