"""
URL configuration for DjangoApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from api.home.home_views import home_view, home_calificaciones, home_aprobados, home_reprobados, home_promedios, home_mapa
from api.login.login_views import login_view, logout_view
from api.Administrador.administrador_views import administrador_view, subir_calificaciones, gestionar_usuarios

urlpatterns = [
    path('', home_view, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Vistas académicas
    path('calificaciones/', home_calificaciones, name='calificaciones'),
    path('aprobados/', home_aprobados, name='aprobados'),
    path('reprobados/', home_reprobados, name='reprobados'),  # <-- Agregado aquí ✅
    path('promedios/', home_promedios, name='promedios'),
    path('mapa/', home_mapa, name='mapa'),  # <-- Agregado aquí ✅



    # Vistas administrativas
    path('administrador/', administrador_view, name='administrador'),
    path('administrador/subir-calificaciones/', subir_calificaciones, name='subir_calificaciones'),
    path('administrador/gestionar-usuarios/', gestionar_usuarios, name='gestionar_usuarios'),
]

