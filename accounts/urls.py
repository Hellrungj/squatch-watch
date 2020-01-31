from django.conf.urls import url
from django.urls import include, path
from . import views    

urlpatterns = [    
    url(r'^login/', views.login_view, name='login_view'),
    url(r'^logout/', views.logout_view, name='logout_view'),
    url(r'^accounts/login/', views.login_view, name='login_view'),
    url(r'^accounts/logout/', views.logout_view, name='logout_view'),
    url(r'^accounts/signup/', views.signup_view, name='signup_view'),
    url(r'^accounts/profile/(?P<id>\d+)/$', views.profile_view, name='profile_view'),
    path('accounts/', include('django.contrib.auth.urls')),
]