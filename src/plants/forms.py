from django import forms

from .models import plants

class PlantForm(forms.ModelForm):
	name= forms.CharField(label= "Plant's Name")
	location= forms.CharField(label= "Where does your plant live? (office, main bedroom, etc.)")
	frequency=forms.IntegerField(label= 'How often (in days) do you water this plant?')
	last_watered= forms.DateField( input_formats=['%m/%d/%Y',],label="When's the last time you watered your plant? (mm/dd/yyyy)")
	class Meta:
		model= plants
		fields= [
			'name',
			'location',
			'frequency',
			'last_watered'

		]

# class RawPlantForm(forms.Form):
# 		name= forms.CharField(label= "Plant's Name")
# 		location= forms.CharField(label= "Where does your plant live? (office, main bedroom, etc.)")
# 		frequency=forms.IntegerField(label= 'How often (in days) do you water this plant?')
# 		last_watered= forms.DateField( label="When's the last time you watered your plant? (mm/dd/yyyy)")