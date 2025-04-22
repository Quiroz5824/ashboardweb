from django.shortcuts import render
from api.models import CicloEscolar, Periodo, CicloPeriodo, ProgramaEducativoAntiguo, ProgramaEducativoNuevo

def examen_admision_view(request):
    mensaje = None

    # Lógica de creación de ciclo/periodo si es POST (la tienes aparte o en esta función)

    # Obtener todos los programas
    programas_antiguos = ProgramaEducativoAntiguo.objects.all()
    programas_nuevos = ProgramaEducativoNuevo.objects.all()

    # Obtener todos los ciclos con periodo
    ciclos_periodos = CicloPeriodo.objects.select_related('ciclo', 'periodo').all()
    anios = sorted(set([str(cp.ciclo.anio) for cp in ciclos_periodos]), reverse=True)

    return render(request, 'examen_admision.html', {
        'mensaje': mensaje,
        'programas_antiguos': programas_antiguos,
        'programas_nuevos': programas_nuevos,
        'anios': anios,
    })
