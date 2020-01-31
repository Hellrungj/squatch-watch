from django.contrib import admin

# Register your models here.
from .models import Monster, Monster_Image, \
                    Researcher, \
                    Sighting, Sighting_Monster, Sighting_Researcher, \
                    MonsterReport, User_MonsterReport, MonsterReport_Sighting

admin.site.register(Monster)
admin.site.register(Monster_Image)

admin.site.register(Researcher)

admin.site.register(Sighting)
admin.site.register(Sighting_Monster)
admin.site.register(Sighting_Researcher)

admin.site.register(MonsterReport)
admin.site.register(User_MonsterReport)
admin.site.register(MonsterReport_Sighting)