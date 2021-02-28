from django.db import models

# Create your models here.
class plants(models.Model):
	name= models.CharField(max_length=50)
	location=models.CharField(max_length=200)
	frequency=models.PositiveSmallIntegerField()
	last_watered=models.DateField()