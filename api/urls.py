from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from . import views
# Tutorial Link
# https://www.django-rest-framework.org/tutorial/quickstart/

router = routers.DefaultRouter()
router.register(r'monster_report', views.MonsterReportViewSet)
router.register(r'sighting', views.SightingViewSet)
router.register(r'researcher', views.ResearcherViewSet)
router.register(r'monster', views.MonsterViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
# Standard Display
    path('', include(router.urls)),     
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]
