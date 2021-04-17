"""pydemande URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from core.views import logoutTlogin

urlpatterns = [
    
    path('', include('core.urls')), 
    
    re_path(r'', include('user_sessions.urls', 'user_sessions')), #user sessions
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logoutTlogin, name='logout'),
    path('demande-summary/logout/', lambda request: redirect('logout', permanent=False)),
    path('rapport/logout/', lambda request: redirect('logout', permanent=False)),
    path('demandes/logout/', lambda request: redirect('logout', permanent=False)),
    path('motifs/logout/', lambda request: redirect('logout', permanent=False)),
    path('motif/logout/', lambda request: redirect('logout', permanent=False)),
    path('demande/logout/', lambda request: redirect('logout', permanent=False)),
    path('demandes/traite/logout/', lambda request: redirect('logout', permanent=False)),
    path(r'', include('qr_code.urls', namespace="qr_code")),
    
    
]

urlpatterns += static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)