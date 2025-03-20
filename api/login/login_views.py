from django.shortcuts import render, redirect
from django.contrib import messages
from api.models import Usuarios
  # Asegúrate de importar tu modelo

def login_view(request):
    template_view = "login.html"
    
    if request.method == 'POST':
        matricula = request.POST['matricula']
        password = request.POST['password']

        try:
            usuario = Usuarios.objects.get(matricula=matricula, password=password)
            # Si encuentra la matrícula y contraseña correcta
            return redirect('administrador')  # Asegúrate de tener esta URL
        except Usuarios.DoesNotExist:
            messages.error(request, '⚠️ Matrícula o contraseña incorrecta ⚠️')
    
    return render(request, template_view)

def logout_view(request):
    # Aquí no necesitas logout de Django si no usas su sistema de usuarios
    return redirect('login')
