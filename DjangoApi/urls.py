from django.contrib import admin
from django.urls import path
from api.home.home_views import home_view, home_calificaciones, home_aprobados, home_reprobados, home_promedios, home_mapa
from api.login.login_views import login_view, logout_view
from api.Administrador.administrador_views import administrador_view, subir_calificaciones, gestionar_usuarios, generar_plantilla_csv
from api.views import egresados_view

from api.Administrador.examen_views import examen_admision_view  # ✅ Importación correcta
from api.Administrador.csv_views import (
    descargar_plantilla_nuevo_ingreso,
    subir_csv_nuevo_ingreso
)
from api.Administrador import matriculagenero_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_view, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('calificaciones/', home_calificaciones, name='calificaciones'),
    path('aprobados/', home_aprobados, name='aprobados'),
    path('reprobados/', home_reprobados, name='reprobados'),
    path('promedios/', home_promedios, name='promedios'),
    path('mapa/', home_mapa, name='mapa'),

    # Vistas de administrador
    path('administrador/', administrador_view, name='administrador'),
    path('administrador/subir-calificaciones/', subir_calificaciones, name='subir_calificaciones'),
    path('administrador/egresados/', egresados_view, name='egresados'),
    path('administrador/gestionar-usuarios/', gestionar_usuarios, name='gestionar_usuarios'),
    path('administrador/generar-plantilla/', generar_plantilla_csv, name='generar_plantilla_csv'),

    path('administrador/descargar-plantilla-nuevo-ingreso/', descargar_plantilla_nuevo_ingreso, name='descargar_plantilla_nuevo_ingreso'),
    path('administrador/subir-csv-nuevo-ingreso/', subir_csv_nuevo_ingreso, name='subir_csv_nuevo_ingreso'),
   
    # ✅ Examen Admisión
# en urls.py
    path('administrador/examen-admision/', examen_admision_view, name='examen_admision'),
    path('administrador/matricula-genero/', matriculagenero_views.matriculagenero, name='matricula_por_genero'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
