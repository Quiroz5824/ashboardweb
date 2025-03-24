from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def administrador_view(request):
    if not request.user.is_staff:
        return redirect('index')
    return render(request, 'administrador.html')

@login_required
def subir_calificaciones(request):
    if not request.user.is_staff:
        return redirect('index')
    if request.method == 'POST':
        # Lógica para subir calificaciones
        return HttpResponse('Calificaciones cargadas correctamente')
    return render(request, 'subir_calificaciones.html')

@login_required
def gestionar_usuarios(request):
    if not request.user.is_staff:
        return redirect('index')
    # Lógica para gestionar usuarios
    return HttpResponse('Gestión de usuarios')
