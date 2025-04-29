from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from api.models import EficienciaTerminal, ProgramaEducativoAntiguo, ProgramaEducativoNuevo, CicloPeriodo
import pandas as pd
import io
import csv

def eficiencia_terminal_view(request):
    mensaje = None
    eficiencia = []
    programas = []
    matriculas = []
    egresados = []
    porcentajes = []

    ciclos_periodos = CicloPeriodo.objects.select_related('ciclo', 'periodo').order_by('-ciclo__anio')
    filtro_id = request.GET.get("filtro_anio")

    if filtro_id and filtro_id != "Todos":
        try:
            ciclo = CicloPeriodo.objects.get(id=filtro_id)
            eficiencia = EficienciaTerminal.objects.filter(ciclo_periodo=ciclo)
            for e in eficiencia:
                nombre = e.programa_antiguo.nombre if e.programa_antiguo else e.programa_nuevo.nombre
                programas.append(nombre)
                matriculas.append(e.matricula_ingreso)
                egresados.append(e.egresados)
                porcentajes.append(e.porcentaje_eficiencia)
        except CicloPeriodo.DoesNotExist:
            messages.warning(request, "⚠️ Ciclo seleccionado no válido.")

    return render(request, 'eficiencia_terminal.html', {
        'mensaje': mensaje,
        'eficiencia': eficiencia,
        'programas': programas,
        'matriculas': matriculas,
        'egresados': egresados,
        'porcentajes': porcentajes,
        'anios': ciclos_periodos
    })

def descargar_plantilla_eficiencia_terminal(request):
    programas_antiguos = list(ProgramaEducativoAntiguo.objects.values_list('nombre', flat=True))
    programas_nuevos = list(ProgramaEducativoNuevo.objects.values_list('nombre', flat=True))
    nombres_programas = sorted(set(programas_antiguos + programas_nuevos))

    df = pd.DataFrame({
        'PROGRAMA EDUCATIVO': nombres_programas,
        'CICLO': [''] * len(nombres_programas),
        'MATRICULA INICIAL': [''] * len(nombres_programas),
        'TOTAL EGRESADOS': [''] * len(nombres_programas)
    })

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename=\"PLANTILLA_EFICIENCIA_TERMINAL.csv\"'
    df.to_csv(path_or_buf=response, index=False, sep=',', encoding='utf-8-sig', quoting=csv.QUOTE_MINIMAL)

    return response

def subir_csv_eficiencia_terminal(request):
    if request.method == 'POST' and request.FILES.get('archivo_csv'):
        archivo = request.FILES['archivo_csv']
        errores = []
        exitosos = 0

        try:
            df = pd.read_csv(archivo, encoding='utf-8-sig')
            for index, fila in df.iterrows():
                fila_num = index + 2
                try:
                    nombre_programa = str(fila['PROGRAMA EDUCATIVO']).strip()
                    clave_ciclo = str(fila['CICLO']).strip()
                    matricula = int(fila['MATRICULA INICIAL'])
                    total_egresados = int(fila['TOTAL EGRESADOS'])

                    ciclo = CicloPeriodo.objects.get(
                        ciclo__anio=int(clave_ciclo.split(' - ')[0]),
                        periodo__clave=clave_ciclo.split(' - ')[1]
                    )

                    programa_antiguo = ProgramaEducativoAntiguo.objects.filter(nombre__iexact=nombre_programa).first()
                    programa_nuevo = ProgramaEducativoNuevo.objects.filter(nombre__iexact=nombre_programa).first()

                    if not programa_antiguo and not programa_nuevo:
                        raise ValueError(f"Programa '{nombre_programa}' no encontrado")

                    EficienciaTerminal.objects.create(
                        ciclo_periodo=ciclo,
                        programa_antiguo=programa_antiguo,
                        programa_nuevo=programa_nuevo,
                        matricula_ingreso=matricula,
                        egresados=total_egresados
                    )
                    exitosos += 1

                except Exception as e:
                    errores.append(f"Fila {fila_num}: {str(e)}")

            if errores:
                messages.warning(request, f"⚠️ Errores:<br>{'<br>'.join(errores)}")
            if exitosos > 0:
                messages.success(request, f"✅ {exitosos} registros guardados correctamente.")

        except Exception as e:
            messages.error(request, f"❌ Error al procesar el archivo: {str(e)}")

    return redirect('eficiencia_terminal')
