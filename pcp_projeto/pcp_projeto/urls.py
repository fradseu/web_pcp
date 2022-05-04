"""pcp_projeto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from core import views
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('teste/', views.teste , name='teste'),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/home/')),
    path('home/', views.home),
    path('ferr_form/', views.ferr_form, name="ferr_form"),
    path('ferr_list/', views.ferr_list, name="ferr_list"),
    path('form/<slug:slug>/', views.ferr_form, name='ferr_form_update'),
    path('<slug:slug>/', views.ferr_detail, name='ferr_detail'),
    

]

urlpatterns += staticfiles_urlpatterns()