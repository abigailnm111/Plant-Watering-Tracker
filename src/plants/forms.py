from django import forms

from .models import plants

class PlantForm(forms.ModelForm):
	class Meta:
		model= plants
		fields= [
			'name',
			'location',
			'frequency',
			'last_watered'

		]

#class RawPlantForm(forms.form):
#	name= forms.CharField(label= "Plant's Name")
#	location= forms.CharField(label= "Where does your plant live? (office, main bedroom, etc.")
#	frequency=forms.IntegerField(label= 'How often (in days) do you water this plant?')
#	last_watered= forms.DateField( label='Whens the last time you watered your plant? (yyy-mm-dd)')