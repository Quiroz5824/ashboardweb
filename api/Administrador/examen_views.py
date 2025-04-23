from django.shortcuts import render
from django.db.models import Sum
from api.models import (
    CicloEscolar, Periodo, CicloPeriodo,
    ProgramaEducativoAntiguo, ProgramaEducativoNuevo, NuevoIngreso
)


def examen_admision_view(request):
    mensaje = None

    if request.method == 'POST' and 'crear_ciclo' in request.POST:
        periodos_definidos = [
            ('E-A', 'Enero - Abril'),
            ('M-A', 'Mayo - Agosto'),
            ('S-D', 'Septiembre - Diciembre')
        ]

        ultimo_ciclo = CicloEscolar.objects.order_by('-anio').first()
        anio_actual = ultimo_ciclo.anio if ultimo_ciclo else 2025
        ciclo_actual, _ = CicloEscolar.objects.get_or_create(anio=anio_actual)

        periodos_actuales = CicloPeriodo.objects.filter(
            ciclo=ciclo_actual
        ).values_list('periodo__clave', flat=True)

        siguiente_periodo = next(
            ((clave, nombre) for clave, nombre in periodos_definidos if clave not in periodos_actuales), None)

        if siguiente_periodo:
            clave, nombre = siguiente_periodo
            periodo, _ = Periodo.objects.get_or_create(clave=clave, defaults={'nombre': nombre})
            CicloPeriodo.objects.get_or_create(ciclo=ciclo_actual, periodo=periodo)
            mensaje = f"✅ Se creó el ciclo {ciclo_actual.anio} periodo {nombre}"
        else:
            nuevo_ciclo, _ = CicloEscolar.objects.get_or_create(anio=anio_actual + 1)
            clave, nombre = periodos_definidos[0]
            periodo, _ = Periodo.objects.get_or_create(clave=clave, defaults={'nombre': nombre})
            CicloPeriodo.objects.get_or_create(ciclo=nuevo_ciclo, periodo=periodo)
            mensaje = f"✅ Se creó el ciclo {nuevo_ciclo.anio} periodo {nombre}"

    # Programas
    programas_antiguos = ProgramaEducativoAntiguo.objects.all()
    programas_nuevos = ProgramaEducativoNuevo.objects.all()

    # Ciclos disponibles (para selector)
    ciclos_periodos = CicloPeriodo.objects.select_related('ciclo', 'periodo')
    opciones_ciclo = sorted(
        [f"{cp.ciclo.anio} - {cp.periodo.clave}" for cp in ciclos_periodos],
        reverse=True
    )

    filtro = request.GET.get("filtro_anio")
    datos_graficas = {}
    detalle_programas = []

    if filtro and filtro != "Todos":
        anio_str, periodo_clave = filtro.split(" - ")
        try:
            ciclo_periodo = CicloPeriodo.objects.select_related("ciclo", "periodo").get(
                ciclo__anio=anio_str, periodo__clave=periodo_clave
            )

            # Totales generales
            datos = NuevoIngreso.objects.filter(ciclo_periodo=ciclo_periodo).aggregate(
                examen=Sum('examen'),
                renoes=Sum('renoes'),
                uaem_gem=Sum('uaem_gem'),
                pase_directo=Sum('pase_directo')
            )
            datos_graficas = datos

            # Detalle por programa
            ingresos = NuevoIngreso.objects.filter(ciclo_periodo=ciclo_periodo).select_related(
                'programa_antiguo', 'programa_nuevo'
            )

            for ingreso in ingresos:
                nombre_programa = ingreso.programa_antiguo.nombre if ingreso.programa_antiguo else ingreso.programa_nuevo.nombre
                detalle_programas.append({
                    'programa': nombre_programa,
                    'examen': ingreso.examen,
                    'renoes': ingreso.renoes,
                    'uaem_gem': ingreso.uaem_gem,
                    'pase_directo': ingreso.pase_directo
                })

        except CicloPeriodo.DoesNotExist:
            pass

    return render(request, 'examen_admision.html', {
        'mensaje': mensaje,
        'programas_antiguos': programas_antiguos,
        'programas_nuevos': programas_nuevos,
        'anios': opciones_ciclo,
        'datos_graficas': datos_graficas,
        'detalle_programas': detalle_programas
    })
