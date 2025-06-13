"""
URL configuration for roombooking project.

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
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions 
from .views import hello
from rest_framework.authtoken.views import obtain_auth_token


schema_view = get_schema_view(
    openapi.Info(
        title="Room Booking API",
        default_version='v1',
        description="API for managing workspace room bookings, cancellations, and availability in a shared office setup.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', hello), #get to home page
    path('admin/', admin.site.urls),
    path('auth-token', obtain_auth_token, name='auth-token'), #post request to get token
    path('api/v1/bookings/', include('bookings.urls')),
    path('api/v1/rooms/', include('rooms.urls')),
    
    # Documentation URLs
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
