"""
URL configuration for fleet_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .api.taxi import get_taxis
from .api.taxi_locations import taxi_locations
from .api.last_taxi_location import last_taxi_location
from .swagger import schema_view

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('taxis/', get_taxis, name='get_taxis'),

    path('taxi_locations/', taxi_locations, name='taxi_locations'),

    path('taxis/<int:taxi_id>/last_location/', last_taxi_location, name='last_taxi_location'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
