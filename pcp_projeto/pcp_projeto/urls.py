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
from core.views import ferram_class, atualizador_class,manut_detail_class
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    #path('manut_list/', views.manut_list, name='manut_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('login/submit', views.submit_login, name='entrar_login'),
    path('teste/', views.teste,name='teste'),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/home/')),
    path('home/', views.home),
    path('ferr_form/', ferram_class.ferr_form, name="ferr_form"),
    path('manut_list/', views.manut_list, name="manut_list"),
    path('form/<slug:slug>/', ferram_class.ferr_form, name='ferr_form_update'),
    path('<slug:slug>/', manut_detail_class.manut_detail, name='manut_detail'),
    path('delete/<int:id>', views.form_delete, name='form_delete'),
    path('apagar/<int:id>', views.apagar_delete, name='apagar_delete'),
    path('impressao/', views.manut_impressao, name='manut_impressao'),
    path('updt_c/<int:id>', atualizador_class.updt_close, name='updt_close'),
    path('updt_o/<int:id>', atualizador_class.updt_open, name='updt_open'),
    
    
    

]

urlpatterns += staticfiles_urlpatterns()
