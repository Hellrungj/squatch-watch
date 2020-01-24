from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
# Standard Display     
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login_view, name='login_view'),
    url(r'^logout/', views.logout_view, name='logout_view'),
    url(r'^accounts/login/', views.login_view, name='login_view'),
    url(r'^accounts/logout/', views.logout_view, name='logout_view'),
    url(r'^accounts/signup/', views.signup_view, name='signup_view'),
    url(r'^report/(?P<id>\d+)/$', views.report_details, name='report_details'),
    url(r'^report/sighting/(?P<id>\d+)/$', views.sighting_details, name='sighting_details'),
    url(r'^report/upload/$', views.upload_csv, name='upload_csv'),
# Searching
    path('search/sighting/<int:id>/', views.search_sighting_id, name='search_sighting_id'),
    path('search/report/<int:id>/', views.search_report_id, name='search_report_id'),

    path('search/researcher/<str:name>/', views.search_researcher, name='search_researcher'),
    path('search/monster/<str:name>/', views.search_monster, name='search_monster'),
    path('search/sighting/<str:title>/', views.search_sighting_title, name='search_sighting_title'),
    path('search/report/<str:title>/', views.search_report_title, name='search_report_title'),
]
