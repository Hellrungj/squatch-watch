from monsters.models import MonsterReport, Sighting, Researcher, Monster, Monster_Image
from rest_framework import viewsets
from api.serializers import MonsterReportSerializer, SightingSerializer, ResearcherSerializer, MonsterSerializer, Monster_ImageSerializer

class MonsterReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MonsterReport.objects.all()
    serializer_class = MonsterReportSerializer

class SightingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Sighting.objects.all()
    serializer_class = SightingSerializer

class ResearcherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Researcher.objects.all()
    serializer_class = ResearcherSerializer

class MonsterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Monster.objects.all()
    serializer_class = MonsterSerializer

class Monster_ImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Monster_Image.objects.all()
    serializer_class = Monster_ImageSerializer