from django.shortcuts import render
from api.models import (
    CicloEscolar,
    Periodo,
    CicloPeriodo,
    ProgramaEducativoAntiguo,
    ProgramaEducativoNuevo,
    NuevoIngreso
)

from collections import defaultdict
import json


def examen_admision_view(request):
    mensaje = None

    if request.method == 'POST':
        periodos_definidos = [
            ('E-A', 'Enero - Abril'),
            ('M-A', 'Mayo - Agosto'),
            ('S-D', 'Septiembre - Diciembre')
        ]

        ultimo_ciclo = CicloEscolar.objects.order_by('-anio').first()
        anio_actual = ultimo_ciclo.anio if ultimo_ciclo else 2025
        anio_actual = int(anio_actual)

        ciclo_actual, _ = CicloEscolar.objects.get_or_create(anio=anio_actual)

        periodos_actuales = CicloPeriodo.objects.filter(
            ciclo=ciclo_actual
        ).values_list('periodo__clave', flat=True)

        siguiente_periodo = None
        for clave, nombre in periodos_definidos:
            if clave not in periodos_actuales:
                siguiente_periodo = (clave, nombre)
                break

        if siguiente_periodo:
            clave, nombre = siguiente_periodo
            periodo, _ = Periodo.objects.get_or_create(clave=clave, defaults={'nombre': nombre})
            CicloPeriodo.objects.get_or_create(ciclo=ciclo_actual, periodo=periodo)
            mensaje = f"✅ Se creó el ciclo {ciclo_actual.anio} periodo {nombre}"
        else:
            nuevo_anio = anio_actual + 1
            nuevo_ciclo, _ = CicloEscolar.objects.get_or_create(anio=nuevo_anio)
            clave, nombre = periodos_definidos[0]
            periodo, _ = Periodo.objects.get_or_create(clave=clave, defaults={'nombre': nombre})
            CicloPeriodo.objects.get_or_create(ciclo=nuevo_ciclo, periodo=periodo)
            mensaje = f"✅ Se creó el ciclo {nuevo_anio} periodo {nombre}"

    programas_antiguos = ProgramaEducativoAntiguo.objects.all()
    programas_nuevos = ProgramaEducativoNuevo.objects.all()

    # Ciclos formateados para el filtro (Ej: 2027 - E-A)
    ciclos_periodos = CicloPeriodo.objects.select_related('ciclo', 'periodo')
    ciclos_display = [f"{cp.ciclo.anio} - {cp.periodo.clave}" for cp in ciclos_periodos]
    ciclos_display.sort(reverse=True)

    # Preparar datos reales para gráficas
    datos_por_ciclo = defaultdict(lambda: {
        'examen': 0, 'renoes': 0, 'uaem_gem': 0, 'pase_directo': 0
    })

    for ni in NuevoIngreso.objects.select_related('ciclo_periodo', 'ciclo_periodo__ciclo', 'ciclo_periodo__periodo'):
        clave_ciclo = f"{ni.ciclo_periodo.ciclo.anio} - {ni.ciclo_periodo.periodo.clave}"
        datos_por_ciclo[clave_ciclo]['examen'] += ni.examen
        datos_por_ciclo[clave_ciclo]['renoes'] += ni.renoes
        datos_por_ciclo[clave_ciclo]['uaem_gem'] += ni.uaem_gem
        datos_por_ciclo[clave_ciclo]['pase_directo'] += ni.pase_directo

    # Serializar datos a JSON
    datos_json = json.dumps(datos_por_ciclo)

    return render(request, 'examen_admision.html', {
        'mensaje': mensaje,
        'programas_antiguos': programas_antiguos,
        'programas_nuevos': programas_nuevos,
        'anios': ciclos_display,
        'datos_json': datos_json
    })
