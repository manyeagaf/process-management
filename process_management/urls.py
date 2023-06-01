"""dept URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from argparse import Namespace
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import dashboard

urlpatterns = [
    
    path('super-admin/', admin.site.urls),
    path('',dashboard),
    path('accounts/', include('users.urls',namespace='users')),
    path('admin/',include('admin_user.urls',namespace='admin_user')),
    path('branch/',include('branch.urls',namespace='branch')), 
    path('officer/',include('officer.urls',namespace = 'officer')),
    path('requests/',include('tickets.urls',namespace = 'tickets')),
    path('access-control/',include('access_control.urls',namespace='superAdmin')),
    path('chat/', include('chat.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
