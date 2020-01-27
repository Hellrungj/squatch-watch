from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField
from django.conf import settings
#MonsterReport: refers to a single CSV report that is comprised of many sightings
#Sighting: an instance of a researcher spotting a monster at a specific time and location
#Researcher: the human credited with finding the monster (unique across all sightings)
#Monster: the monster spotted (unique across all sightings)

# Create your models here.
class Monster(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=150, null=True)
    height = models.DecimalField(max_digits = 5, decimal_places = 3, default= 000.00)
    width = models.DecimalField(max_digits = 6, decimal_places = 4, default= 0000.00)
    weight = models.DecimalField(max_digits = 6, decimal_places = 4, default= 0000.00)
    def __str__(self):
        return self.name

class Monster_Image(models.Model):
    monster_id = models.ForeignKey(Monster, on_delete = models.CASCADE, null=True)
    image = ImageField(upload_to=settings.MEDIA_MONSTER_IMAGE_URL[1:-1], blank=True, null=True)

class Researcher(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Sighting(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=150, null=True)
    sighted = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.title

class Sighting_Monster(models.Model):
    sighting = models.ForeignKey(Sighting, on_delete = models.CASCADE, null=True)
    monster = models.ForeignKey(Monster, on_delete = models.CASCADE, null=True)

class Sighting_Researcher(models.Model):
    sighting = models.ForeignKey(Sighting, on_delete = models.CASCADE, null=True)
    researcher = models.ForeignKey(Researcher, on_delete = models.CASCADE, null=True)

class MonsterReport(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=150, null=True)
    report = models.FileField(upload_to=settings.MEDIA_REPORT_URL[1:-1], null=True)
    def __str__(self):
        return self.title

# https://stackoverflow.com/questions/44342921/storing-data-from-a-csv-file-into-a-database

class User_MonsterReport(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    monsterReport = models.ForeignKey(MonsterReport, on_delete = models.CASCADE, null=True)

class MonsterReport_Sighting(models.Model):
    monsterReport = models.ForeignKey(MonsterReport, on_delete = models.CASCADE, null=True)
    sighting = models.ForeignKey(Sighting, on_delete = models.CASCADE, null=True)
 