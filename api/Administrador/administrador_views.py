import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings

def subir_calificaciones(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    if request.method == 'POST' and request.FILES.get('archivo_excel'):
        excel_file = request.FILES['archivo_excel']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'excels'))
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        try:
            df = pd.read_excel(file_path)
            print(df.head())  # Aquí ves si se cargó correctamente
            # Aquí puedes hacer lo que quieras con los datos (guardar, graficar, etc.)
            return HttpResponse("Archivo Excel cargado con éxito.")
        except Exception as e:
            return HttpResponse(f"Error al procesar el archivo: {e}")

    return render(request, 'subir_calificaciones.html')

def administrador_view(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    return render(request, 'administrador.html')

def gestionar_usuarios(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    return HttpResponse('Gestión de usuarios')