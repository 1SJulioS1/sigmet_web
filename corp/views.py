from django.shortcuts import render
from django.views.generic import ListView

from corp.models import *


class InstrumentoListView(ListView):
    model = Instrumentos
    context_object_name = 'object'
    ordering = ['instnom']
    template_name = 'corp/index.html'


def cant_inst(request):
    cant_instr = Instrumentos.objects.count()
    cant_instr_an = Instrumentos.objects.filter(instindvisual='Analógico').count()
    cant_instr_dig = Instrumentos.objects.filter(instindvisual='Digital').count()

    # Cantidad de instrumentos por magnitudes
    instr_por_mag = []
    for i in Magnitudes.objects.all():
        instr_por_mag.append((i.magnom, Instrumentos.objects.filter(idmag=i).count()))

    # Cantidad de Instrumentos por grupos de magnitudes
    instr_por_grp_mag = []
    for i in Gruposmagnitudes.objects.all():
        instr_por_grp_mag.append(
            (i.grpmagnom, Instrumentos.objects.filter(idmag__grpmagnom__grpmagnom=i.grpmagnom).count()))

    # Cantidad de instrumentos por Magnitudes del grupo de magnitudes Electricidad
    instr_por_mag_elect = []
    for i in Magnitudes.objects.filter(grpmagnom__grpmagnom='Electricidad'):
        instr_por_mag_elect.append((i.magnom, Instrumentos.objects.filter(idmag=i).count()))

    rango_medicion_1 = []
    # for i in Caracteristicasmetrologicas.objects.filter(idrngmed__rngmedliminf=0).filter(idrngmed__rngmedlimsup=150):
    #   if i.idinst not i.idinst
    #
    # mag_volt = []
    # for i in Relacionmagnitudesunidadesmedicion.objects.filter(idunimed__unimedsim='V').f:
    #     Magnitudes.objects.filter(i)

    # Cantidad de instrumentos de frecuencia
    instr_por_mag_frec = Instrumentos.objects.filter(idmag__magnom='Frecuencia').count()

    # Determinar cantidad de instrumentos de la magnitud dimensional que sean Pie de Rey
    cant_instr_dim = Instrumentos.objects.filter(idmag__grpmagnom__grpmagnom='Dimensional').filter(
        instnom='Pie de Rey').count()

    # Determinar cantidad de Instrumentos cuyo nombre sea Cintas métricas(Revisar variantes de nombres)
    cant_cintas = Instrumentos.objects.filter(instnom__contains='Cinta métrica').count()

    # Determinar cantidad de Instrumentos cuyo nombre sea Medidores de nivel(Revisar variantes de nombres)
    cant_medidor_nivel = Instrumentos.objects.filter(instnom__contains='Medidor de nivel').count()

    # Determinar cantidad de Instrumentos cuyo nombre sea Medidores de ángulos(Revisar variantes de nombres)
    cant_medidor_angulo = Instrumentos.objects.filter(instnom__contains='Medidor de ángulos').count()

    # Determinar cantidad de Instrumentos cuyo nombre sea Comparadores de carátulas(Revisar variantes de nombres)
    cant_comparador_caratula = Instrumentos.objects.filter(instnom__contains='Comparadores de carátulas').count()

    # Determinar cantidad de Instrumentos cuyo nombre sea Reglas(Revisar variantes de nombres)
    cant_regla = Instrumentos.objects.filter(instnom__contains='Regla').count()

    # Determinar cantidad de Instrumentos cuyo nombre sea Galgas(Revisar variantes de nombres)
    cant_galga = Instrumentos.objects.filter(instnom__contains='Galga').count()

    # Determinar Cantidad de patrones de electricidad
    cant_patr_electricidad = Instrumentos.objects.filter(catusonom__catusonom='Patrón').filter(
        idmag__grpmagnom__grpmagnom='Electricidad').count()

    # Determinar Cantidad de patrones de Electricidad con magnitud especifica Tension
    cant_patr_tension = Instrumentos.objects.filter(catusonom__catusonom='Patrón').filter(
        idmag__magnom='Tensión eléctrica').count()

    # Determinar Cantidad de patrones de Electricidad con magnitud especifica Resistencia
    cant_patr_resistencia = Instrumentos.objects.filter(catusonom__catusonom='Patrón').filter(
        idmag__magnom='Resistencia Eléctrica').count()

    # Determinar Cantidad de patrones de Presión
    cant_patr_presion = Instrumentos.objects.filter(catusonom__catusonom='Patrón').filter(
        idmag__magnom='Presión').count()

    # Determinar Cantidad de patrones de Temperatura
    cant_patr_temperatura = Instrumentos.objects.filter(catusonom__catusonom='Patrón').filter(
        idmag__magnom='Temperatura').count()

    return render(request, 'corp/index.html',
                  {'cant_instr': cant_instr, 'cant_instr_an': cant_instr_an, 'cant_instr_dig': cant_instr_dig,
                   'numero_inst_mag': instr_por_mag, 'numero_inst_mag_elec': instr_por_mag_elect,
                   'instr_por_grp_mag': instr_por_grp_mag, 'instr_por_mag_frec': instr_por_mag_frec,
                   'cant_instr_dim': cant_instr_dim,
                   'cant_cintas': cant_cintas,
                   'cant_medidor_nivel': cant_medidor_nivel,
                   'cant_medidor_angulo': cant_medidor_angulo,
                   'cant_comparador_caratula': cant_comparador_caratula,
                   'cant_regla': cant_regla,
                   'cant_galga': cant_galga,
                   'cant_patr_electricidad': cant_patr_electricidad,
                   'cant_patr_tension': cant_patr_tension,
                   'cant_patr_resistencia': cant_patr_resistencia,
                   'cant_patr_presion': cant_patr_presion,
                   'cant_patr_temperatura': cant_patr_temperatura,
                   })
