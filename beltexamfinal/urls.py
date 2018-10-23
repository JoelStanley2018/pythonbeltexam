"""beltexamfinal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from myapp import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^user_dash', views.user_dash),
    url(r'^new_user$', views.new_user),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^create_trip$', views.create_trip),
    url(r'^make_trip$', views.make_trip),
    url(r'^join/(?P<trip_id>\d+)$', views.join),
    url(r'^show/(?P<trip_id>\d+)$', views.show),
    
]
