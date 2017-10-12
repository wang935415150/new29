"""auto_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^index.html$', views.index),
    url(r'^index_ajax.html$', views.index_ajax),
    url(r'^disk.html$', views.disk),
    url(r'^disk_ajax.html$', views.disk_ajax),
    url(r'^nic.html$', views.nic),
    url(r'^nic_ajax.html$', views.nic_ajax),

    url(r'^test.html$', views.test),
]
