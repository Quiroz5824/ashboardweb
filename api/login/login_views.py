from django.shortcuts import render, redirect
from django.contrib import messages
from api.models import Usuarios

def login_view(request):
    template_view = "login.html"
    
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        password = request.POST.get('password')

        try:
            usuario = Usuarios.objects.get(matricula=matricula, password=password)
            # Guardar en sesión
            request.session['usuario_id'] = usuario.usuario_id
            request.session['matricula'] = usuario.matricula
            request.session['nombre'] = usuario.nombre

            return redirect('administrador')
        except Usuarios.DoesNotExist:
            messages.error(request, '⚠️ Matrícula o contraseña incorrecta ⚠️')

    return render(request, template_view)

def logout_view(request):
    request.session.flush()  # Elimina toda la sesión
    return redirect('login')