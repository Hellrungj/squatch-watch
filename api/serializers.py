from monsters.models import MonsterReport, Sighting, Researcher, Monster, Monster_Image
from rest_framework import serializers

class MonsterReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MonsterReport
        fields = ['title','description','report','sighting']

class SightingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sighting
        fields = ['title','description','sighted','researcher','monster']
        

class ResearcherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Researcher
        fields = ['name']

class MonsterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Monster
        fields = ['name','description','height','width','weight','images']

class Monster_ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Monster_Image
        fields = ['title','image']
