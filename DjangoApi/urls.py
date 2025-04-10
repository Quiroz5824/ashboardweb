from django.contrib import admin
from django.urls import path
from api.home.home_views import home_view, home_calificaciones, home_aprobados, home_reprobados, home_promedios, home_mapa
from api.login.login_views import login_view, logout_view
from api.Administrador.administrador_views import administrador_view, subir_calificaciones, gestionar_usuarios, generar_plantilla_csv

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
    path('administrador/gestionar-usuarios/', gestionar_usuarios, name='gestionar_usuarios'),
    path('administrador/generar-plantilla/', generar_plantilla_csv, name='generar_plantilla_csv'),  # 🟢 Esta línea es la que te faltaba
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
