from django.db import models

from django.urls import reverse

from django.contrib.auth.models import User

# Create your models here.
class plants(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	name= models.CharField(max_length=50)
	location=models.CharField(max_length=200)
	frequency=models.PositiveSmallIntegerField()
	last_watered=models.DateField()
	event_id = models.CharField(max_length= 50, blank=True)

	def get_absolute_url(self):
		return reverse('update-plant', kwargs={"pk": self.pk})

	def get_delete(self):
		return reverse('delete-plant', kwargs={"pk": self.pk})
