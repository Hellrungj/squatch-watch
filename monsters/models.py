from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

#MonsterReport: refers to a single CSV report that is comprised of many sightings
#Sighting: an instance of a researcher spotting a monster at a specific time and location
#Researcher: the human credited with finding the monster (unique across all sightings)
#Monster: the monster spotted (unique across all sightings)

# Create your models here.

class Researcher(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Monster(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Sighting(models.Model):
    title = models.CharField(max_length=200)
    researcher = models.ManyToManyField(Researcher)#REF researcher
    monster = models.ManyToManyField(Monster) #REF montster
    timestamp = models.DateTimeField(default=datetime.now)
    latitude = models.FloatField()
    longitude = models.FloatField()
    def __str__(self):
        return self.title

class MonsterReport(models.Model):
    title = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    sighting = models.ManyToManyField(Sighting) #REF Sighting
    user = models.OneToOneField(User, on_delete=models.CASCADE,default="")
    def __str__(self):
        return self.title

# https://stackoverflow.com/questions/44342921/storing-data-from-a-csv-file-into-a-database