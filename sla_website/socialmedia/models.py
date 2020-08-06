from django.db import models
from django.urls import reverse
import datetime
from django.utils import timezone

class Acts(models.Model):
	actType = models.CharField(max_length=100, unique=True)

	#string representation of the db
	def __str__(self):
		return self.actType

class CustomUser(models.Model):
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=40)

	def __str__(self):
		return self.username 


class Post(models.Model):
	act = models.ForeignKey(Acts, on_delete = models.CASCADE)
	user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null=True)

	#for actID, we use default ID Django gives for each model
	#name = models.CharField(max_length=100)
	caption = models.CharField(max_length=1000)
	#image = models.FileField()

	image = models.CharField(max_length = 2**32)
	upvotes = models.IntegerField(default = 0)
	timestamp = models.DateTimeField(default = timezone.now(), null = True)


	def get_absolute_url(self):
		return reverse('socialmedia:index')#, kwargs={'pk': self.pk})

	def __str__(self):
		return str(self.id) + ' - ' + self.act.actType

