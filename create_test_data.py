from .models import MonsterReport, Sighting, Researcher, Monster, Monster_Image

# TODO: Create a script the load some data in the database for testing

# This might be the better solution: https://docs.djangoproject.com/en/3.0/howto/initial-data/
# Emample: https://realpython.com/django-pytest-fixtures/

# Create a quick record to setup and test the UI manually
MI = Monster_Image.objects.create(title="Big Foot")
MI.save()

M = Monster.objects.create(name="Big Foot", description="Scary Big Foot!", height=0.5,width=2,weight=14,images=MI)
M.save()

R = Researcher.objects.create(name="John Hellrung")
R.save()

S = Sighting.objects.create(title="Sighting #1", description="I was sitting at my desk when I saw Big Foot!", sighted="2020-04-22 05:14:17", researcher=R, monster=M)
S.save()

MR = MonsterReport.objects.create(title="Report #1", description="This is my first report!", sighting=S) 
MR.save()