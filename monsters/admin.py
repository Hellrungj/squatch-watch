from django.contrib import admin

# Register your models here.
from .models import Monster_Image, \
                    Monster, \
                    Researcher, \
                    Sighting,  \
                    MonsterReport

admin.site.register(Monster_Image)
admin.site.register(Monster)
admin.site.register(Researcher)
admin.site.register(Sighting)
admin.site.register(MonsterReport)