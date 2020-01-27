from monsters.models import MonsterReport, Sighting, Researcher, Monster
from rest_framework import serializers

class MonsterReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MonsterReport
        fields = ['title','filename','path','sighting','user']

class SightingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sighting
        fields = ['title','researcher','monster','timestamp','latitude','longitude']
        

class ResearcherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Researcher
        fields = ['name']

class MonsterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Monster
        fields = ['name']
