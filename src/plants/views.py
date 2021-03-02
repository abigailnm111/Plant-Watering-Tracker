from django.http import Http404
from django.shortcuts import render, get_object_or_404

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
	obj= get_object_or_404(plants, id=id)
	if request.method== 'POST':
		obj.delete()

	context= {
		"object":obj
	}
	return render(request,'plants/plant_delete_view.html', context)

def dynamic_lookup_view(request, id):
	try:
		obj = plants.objects.get(id=id)
	except plants.DoesNotExist:
		raise Http404
	context= {
		'object':obj
	}
	return render(request, "plants/plants_detail.html", context)
