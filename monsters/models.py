from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
#MonsterReport: refers to a single CSV report that is comprised of many sightings
#Sighting: an instance of a researcher spotting a monster at a specific time and location
#Researcher: the human credited with finding the monster (unique across all sightings)
#Monster: the monster spotted (unique across all sightings)

# Create your models here.
class Monster_Image(models.Model):
    title = models.CharField(max_length=200, default="untilted")
    image = models.ImageField(upload_to='media/monsters/images/', blank=True, null=True)

    def __str__(self):
        return self.title

class Monster(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=150, null=True)
    height = models.DecimalField(max_digits = 5, decimal_places = 3, default= 000.00)
    width = models.DecimalField(max_digits = 6, decimal_places = 4, default= 0000.00)
    weight = models.DecimalField(max_digits = 6, decimal_places = 4, default= 0000.00)
    images = models.ManyToManyField(Monster_Image)
    def __str__(self):
        return self.name

class Researcher(models.Model):
    name = models.CharField(max_length=200)  
    def __str__(self):
        return self.name

class Sighting(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=150, null=True)
    sighted = models.DateTimeField(default=datetime.now)
    researcher = models.ManyToManyField(Researcher)
    monster = models.ManyToManyField(Monster)
    def __str__(self):
        return self.title

class MonsterReport(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=150, null=True)
    report = models.FileField(upload_to=settings.MEDIA_REPORT_URL[1:-1], null=True)
    sighting = models.ManyToManyField(Sighting)

    def __str__(self):
        return self.title

# https://stackoverflow.com/questions/44342921/storing-data-from-a-csv-file-into-a-database
