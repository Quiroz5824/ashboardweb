from django.shortcuts import render

def administrador_view(request):
    template_name = 'administrador.html'
    
    return render(request, template_name)