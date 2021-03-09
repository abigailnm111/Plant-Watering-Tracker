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
import oauth_json

#oauth imports
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken, SocialApp


def get_success_url():
		return reverse('plants')

class PlantListView(ListView):
	template_name= 'plants/plants_list.html'
	queryset = plants.objects.all()



# class PlantCreateView(CreateView):
# 	template_name= 'plants/plants_create.html'
# 	form_class= PlantForm
# 	queryset= plants.objects.all()

def plant_create_view(request):
	form=PlantForm(request.POST or None)
	if form.is_valid():
		form.save()
		form= PlantForm()
	context = {
	'form':form
	}
	token = SocialToken.objects.get(account__user=request.user, account__provider='google')
	credentials = Credentials(
		token=token.token,
		refresh_token=token.token_secret,
		token_uri='https://oauth2.googleapis.com/token',
		client_id='799544582104-gbpau73rvg05q41feqi11kc1t6odkkqb.apps.googleusercontent.com', 
		client_secret='oauth_jason.client_secret'
		) 
	service = build('calendar', 'v3', credentials=credentials)
	#NEED TO ADD SCOPES
	test= service.calendars().get(calendarId='primary').execute()
	print(test)
	return render (request, "plants/plants_create.html",context)
	

	


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


