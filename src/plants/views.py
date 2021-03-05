from django.urls import reverse
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
	CreateView,
	ListView,
	UpdateView, 
	DeleteView
	)

from .forms import PlantForm
from .models import plants
# Create your views here.
import Starter_plant

def get_success_url():
		return reverse('plants')

class PlantListView(ListView):
	template_name= 'plants/plants_list.html'
	queryset = plants.objects.all()



class PlantCreateView(CreateView):
	template_name= 'plants/plants_create.html'
	form_class= PlantForm
	queryset= plants.objects.all()
	Starter_plant.oauth()
	def form_valid(self, form):
		print(form.cleaned_data)


class PlantUpdateView(UpdateView):
	template_name= 'plants/plants_create.html'
	form_class= PlantForm
	queryset= plants.objects.all()
	
	def get_success_url(self):
		return reverse('plants')


class PlantDeleteView(DeleteView):
	template_name= 'plants/plants_delete.html'
	queryset= plants.objects.all()
	
	def get_success_url(self):
		return reverse('plants')
	






# def plant_delete_view(request, id):
# 	obj= get_object_or_404(plants, id=id)
# 	if request.method== 'POST':
# 		obj.delete()

# 	context= {
# 		"object":obj
# 	}
# 	return render(request,'plants/plant_delete_view.html', context)


