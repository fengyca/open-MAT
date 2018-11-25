# coding:utf-8
"""fengycaOBJ URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from apps.appcrawler import views as CR
from django.views import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^appcrawler$', CR.getHTML),
    url(r'^$', CR.getHTML),
    url(r'^appcrawler/', include('apps.appcrawler.urls')),

]

if settings.DEBUG is False:
    urlpatterns += [url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT, })]