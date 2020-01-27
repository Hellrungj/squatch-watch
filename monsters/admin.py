from django.contrib import admin

# Register your models here.
from .models import Researcher, Monster, Sighting, MonsterReport

admin.site.register(Researcher)
admin.site.register(Monster)
admin.site.register(Sighting)
admin.site.register(MonsterReport)