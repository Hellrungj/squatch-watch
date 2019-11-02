from django.contrib import admin

# Register your models here.
from .models import Researcher
from .models import Monster
from .models import Sighting
from .models import MonsterReport

admin.site.register(Researcher)
admin.site.register(Monster)
admin.site.register(Sighting)
admin.site.register(MonsterReport)