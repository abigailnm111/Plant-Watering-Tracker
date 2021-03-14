from django.urls import reverse
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
	
	ListView,
	
	)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin	

from .forms import PlantForm
from .models import plants
# Create your views here.
import event_actions


#oauth imports
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken, SocialApp


def get_token(request):
	token = SocialToken.objects.get(account__user=request.user, account__provider='google')
	credentials = Credentials(
		token=token.token,
		refresh_token=token.token_secret,
		token_uri='https://oauth2.googleapis.com/token',
		client_id='799544582104-gbpau73rvg05q41feqi11kc1t6odkkqb.apps.googleusercontent.com', 
		client_secret=''
		) 
	return build('calendar', 'v3', credentials=credentials)


class PlantListView(LoginRequiredMixin,ListView):
	template_name= 'plants/plants_list.html'
	def get_queryset(self):
		return plants.objects.filter(user=self.request.user)



# class PlantCreateView(CreateView):
# 	template_name= 'plants/plants_create.html'
# 	form_class= PlantForm
# 	queryset= plants.objects.all()

@login_required
def plant_create_view(request):
	
	service=get_token(request)
	form=PlantForm(request.POST or None)
	if form.is_valid():

		new_plant=form.save(commit=False)
		new_plant.user= request.user
		event=event_actions.create_event(form.cleaned_data['name'], form.cleaned_data['location'], form.cleaned_data['last_watered'], form.cleaned_data['frequency'],service)
		new_plant.event_id= event['id']
		new_plant=form.save()
		form= PlantForm()
		return redirect('plants')
	context = {
	'form':form
	}
	return render (request, "plants/plants_create.html",context)
	
@login_required
def plant_update_view(request, pk):
	service=get_token(request)
	obj= plants.objects.get(pk=pk)
	form=PlantForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
		if form.has_changed()== True:
			updates_made= []
			for update in form.changed_data:
				updates_made.append(form.cleaned_data[update])
		event_id= getattr(obj, 'event_id')
		
		event_actions.update_event(event_id, form.changed_data, updates_made, service)
		return redirect('plants')
	context= {
	'form': form
	}
	return render(request, "plants/plants_create.html", context)

@login_required
def plant_delete_view(request, pk):
	service=get_token(request)
	obj= get_object_or_404(plants, pk=pk)
	if request.method== 'POST':
		obj.delete()
		event_id= getattr(obj, 'event_id')
		event_actions.delete_event(event_id, service)
		return redirect('plants')
	context= {
		"object":obj
	}
	return render(request,'plants/plants_delete.html', context)

# class PlantUpdateView(UpdateView):
# 	template_name= 'plants/plants_create.html'
# 	form_class= PlantForm
# 	queryset= plants.objects.all()
	
# 	def get_success_url(self):
# 		return reverse('plants')


# class PlantDeleteView(DeleteView):
# 	template_name= 'plants/plants_delete.html'
# 	queryset= plants.objects.all()
	
# 	def get_success_url(self):
# 		return reverse('plants')
	








