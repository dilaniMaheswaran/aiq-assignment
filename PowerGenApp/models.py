from django.db import models


# Create your models here.

class PowerPlants(models.Model):
    _id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=3)
    name = models.CharField(max_length=250)
    net_generation = models.FloatField()
