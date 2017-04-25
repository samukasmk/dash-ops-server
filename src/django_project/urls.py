"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.views.generic import RedirectView
from powerdns_api.views import records, domains, domain_records, rundeck_nodes_by_domain

urlpatterns = [
    url(r'^admin/',    admin.site.urls),
    url(r'^powerdns/', include('powerdns_manager.urls')),
    url(r'^$',         RedirectView.as_view(url='/admin')),
    # Simple API entries
    url(r'^api/inventory/', include('dash_ops_inventory.urls')),
    url(r'^api/powerdns/',  include('powerdns_api.urls')),
]
