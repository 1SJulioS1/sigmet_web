import os
from sigmet.decorators import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from corp.auxiliar_functions import *

@role_required(allowed_roles=['Ejecutivo', 'Administrador'])
def principal(request):
    if request.POST:
        username = request.POST['user']
        password = request.POST['password']

        user = authenticate(request=None, username=username, password=password)
        if user is not None:
            login(request, user)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            content = {
                'invalid_login': True,
                'msg': 'Usuario no válido'
            }
            return render(request, 'corp/principal.html', content)
        else:
            if check_password(password, user.password):
                return HttpResponseRedirect(reverse('corp:index'))
            else:
                content = {
                    'invalid_login': True,
                    'msg': 'Contraseña incorrecta'
                }
                return render(request, 'corp/principal.html', content)
    return render(request, 'corp/principal.html')

@role_required(allowed_roles=['Ejecutivo', 'Administrador'])
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('corp:principal'))

@role_required(allowed_roles=['Ejecutivo', 'Administrador'])
def cant_inst(request):
    return render(request, 'corp/index.html')


@role_required(allowed_roles=['Ejecutivo', 'Administrador'])
def generalidades_instrumento(request):
    instr_single = remove_duplicated_instruments()
    magns = remove_duplicated_magnitudes()
    cant_instr = 0
    lista1, lista2, lista3, lista4 = obtener_instrumento_fabricante(instr_single)
    cant_inst_multifunc_elect_uso = 0
    cant_inst_multifunc_elect_almacenado = 0
    cant_inst_multifunc_nom_dif_uso = 0
    cant_inst_multifunc_nom_dif_almacenado = 0
    cant_uso = 0
    cant_roto = 0
    cant_alm = 0
    inst_uso = dict()
    inst_alm = dict()
    inst_roto = dict()
    multi_elect_uso = dict()
    multi_elect_alm = dict()
    multi_nom_dif_uso = dict()
    multi_nom_dif_alm = dict()

    for ins in instr_single:
        cant_instr += 1
        for m in magns:
            # print(str(m.idmag) + ' : ' + str(m.grpmagnom.grpmagnom))
            if m.grpmagnom.grpmagnom == 'Electricidad' and ins.idmag_id == m.idmag and ins.magiddb_id == m.magiddb:
                if ins.instdescripcion == 'Multifunción con 2 o 3 magnitudes eléctricas':
                    if ins.estadoinstnom.estadoinstnom == 'Uso':
                        cant_inst_multifunc_elect_uso += 1
                        multi_elect_uso = more_info(ins, multi_elect_uso)
                    else:
                        if ins.estadoinstnom.estadoinstnom == 'Almacenado':
                            cant_inst_multifunc_elect_almacenado += 1
                            multi_elect_alm = more_info(ins, multi_elect_alm)
                break
        if ins.instdescripcion == 'Multifunción con 2 o 3 nomenclaturas diferentes':
            if ins.estadoinstnom.estadoinstnom == 'Uso':
                cant_inst_multifunc_nom_dif_uso += 1
                multi_nom_dif_uso = more_info(ins, multi_nom_dif_uso)
            else:
                if ins.estadoinstnom.estadoinstnom == 'Almacenado':
                    cant_inst_multifunc_nom_dif_almacenado += 1
                    multi_nom_dif_alm = more_info(ins, multi_nom_dif_alm)
        if ins.estadoinstnom.estadoinstnom == 'Uso':
            cant_uso += 1
            inst_uso = more_info(ins, inst_uso)
        else:
            if ins.estadoinstnom.estadoinstnom == 'Almacenado':
                cant_alm += 1
                inst_alm = more_info(ins, inst_alm)
            else:
                if ins.estadoinstnom.estadoinstnom == 'Roto':
                    cant_roto += 1
                    inst_roto = more_info(ins, inst_roto)

    return render(request, 'corp/generalidades/gen.html', {'cantidad_instrumentos': cant_instr,
                                                           'cant_inst_multifunc_elect_uso': cant_inst_multifunc_elect_uso,
                                                           'cant_inst_multifunc_elect_almacenado': cant_inst_multifunc_elect_almacenado,
                                                           'cant_inst_multifunc_nom_dif_uso': cant_inst_multifunc_nom_dif_uso,
                                                           'cant_inst_multifunc_nom_dif_almacenado': cant_inst_multifunc_nom_dif_almacenado,
                                                           'lista1': lista1,
                                                           'lista2': lista2,
                                                           'lista3': lista3,
                                                           'lista4': lista4,
                                                           'cant_uso': cant_uso,
                                                           'inst_uso': json.dumps(inst_uso),
                                                           'cant_roto': cant_roto,
                                                           'inst_roto': json.dumps(inst_roto),
                                                           'cant_alm': cant_alm,
                                                           'inst_alm': json.dumps(inst_alm),
                                                           'multi_elect_uso': json.dumps(multi_elect_uso),
                                                           'multi_elect_alm': json.dumps(multi_elect_alm),
                                                           'multi_nom_dif_uso': json.dumps(multi_nom_dif_uso),
                                                           'multi_nom_dif_alm': json.dumps(multi_nom_dif_alm)
                                                           })


@role_required(allowed_roles=['Ejecutivo', 'Administrador'])
def magnitud_instrumento(request):
    inst_per_magn_per_group = instrumentos_por_magnitud()

    return render(request, 'corp/magnitud/magn.html', {'ipmpg': inst_per_magn_per_group,
                                                       })


@role_required(allowed_roles=['Ejecutivo', 'Administrador'])
def instrumentos_trabajo_gen(request):
    instr_single = remove_duplicated_instruments()
    magns = remove_duplicated_magnitudes()

    cant_trab = 0
    inst_trab_more_info = dict()

    count_vacuometro = 0
    inst_vacuometro_more_info = dict()

    count_pie_rey = 0
    inst_pie_rey_more_info = dict()

    count_pie_rey_profundidad = 0
    inst_pie_rey_profundidad_more_info = dict()

    count_micrometro = 0
    inst_micrometro_more_info = dict()

    cant_cintas = 0
    inst_cintas_more_info = dict()

    cant_medidor_nivel = 0
    inst_medidor_nivel_more_info = dict()

    cant_medidor_angulo = 0
    inst_medidor_angulo_more_info = dict()

    cant_comparador_caratula = 0
    inst_comparador_caraturla_more_info = dict()

    cant_regla = 0
    inst_regla_more_info = dict()

    cant_galga = 0
    inst_galga_more_info = dict()

    cant_ttr = 0
    inst_ttr_more_info = dict()

    cant_armonico = 0
    inst_armonico_more_info = dict()

    cant_multif = 0
    inst_multif_more_info = dict()

    count_mag_frec = 0
    inst_mag_frec_more_info = dict()

    inst_tension_subset = []
    instr_micrometro = []
    instrumentos_grupo_presion = []
    instr_trab = []

    for ins in instr_single:
        if ins.catusonom.catusonom == 'Trabajo':
            cant_trab += 1
            inst_trab_more_info = more_info(ins, inst_trab_more_info)
            instr_trab.append(ins)
            if ins.instnom.__contains__('Voltimetro') or ins.instnom.__contains__('Voltímetro'):
                inst_tension_subset.append(ins)
            if ins.instnom.__contains__('Vacuómetro') or ins.instnom.__contains__('Vacuometro'):
                count_vacuometro += 1
                inst_vacuometro_more_info = more_info(ins, inst_vacuometro_more_info)
            if ins.instnom.__contains__('Pie de rey') or ins.instnom.__contains__('pie de rey'):
                count_pie_rey += 1
                inst_pie_rey_more_info = more_info(ins, inst_pie_rey_more_info)

                for m in magns:
                    if m.magnom == 'Profundidad':
                        if ins.idmag_id == m.idmag and ins.magiddb_id == m.magiddb:
                            count_pie_rey_profundidad += 1
                            inst_pie_rey_profundidad_more_info = more_info(ins, inst_pie_rey_profundidad_more_info)
                            break
            if ins.instnom.__contains__('Micrómetro'):
                instr_micrometro.append(ins)
                count_micrometro += 1
                inst_micrometro_more_info = more_info(ins, inst_micrometro_more_info)
            if ins.instnom.__contains__('Cinta métrica'):
                cant_cintas += 1
                inst_cintas_more_info = more_info(ins, inst_cintas_more_info)
            if ins.instnom.__contains__('Medidor de nivel'):
                cant_medidor_nivel += 1
                inst_medidor_nivel_more_info = more_info(ins, inst_medidor_nivel_more_info)
            if ins.instnom.__contains__('Medidor de ángulo'):
                cant_medidor_angulo += 1
                inst_medidor_angulo_more_info = more_info(ins, inst_medidor_angulo_more_info)
            if ins.instnom.__contains__('Comparador de carátulas'):
                cant_comparador_caratula += 1
                inst_comparador_caraturla_more_info = more_info(ins, inst_comparador_caraturla_more_info)
            if ins.instnom.__contains__('Regla'):
                cant_regla += 1
                inst_regla_more_info = more_info(ins, inst_regla_more_info)
            if ins.instnom.__contains__('Galga'):
                cant_galga += 1
                inst_galga_more_info = more_info(ins, inst_galga_more_info)
            if ins.instnom == 'Medidor de Relación de Transformación':
                cant_ttr += 1
                inst_ttr_more_info = more_info(ins, inst_ttr_more_info)
            if ins.instnom.__contains__('Medidor de armónico'):
                cant_armonico += 1
                inst_armonico_more_info = more_info(ins, inst_armonico_more_info)
            if ins.instdescripcion is not None:
                if ins.instdescripcion.__contains__('Multifunción'):
                    cant_multif += 1
                    inst_multif_more_info = more_info(ins, inst_multif_more_info)
            for m in magns:
                if m.magnom == 'Frecuencia':
                    if m.idmag == ins.idmag_id and m.magiddb == ins.magiddb_id:
                        count_mag_frec += 1
                        inst_mag_frec_more_info = more_info(ins, inst_mag_frec_more_info)

    miliohm_lista, ohm_lista, kiloohm_lista, megaohm_lista = instrumentos_medidores_resistencia(instr_trab)

    # Obtener instrumentos de tensiÃ³n existentes por niveles 1kV-5kV
    inst_1_kV = obtener_instrumentos_rango(-1000000, 1, 'kV', inst_tension_subset)

    inst_1_5_kV = obtener_instrumentos_rango(1, 5, 'kV', inst_tension_subset)

    # Obtener instrumentos de tensiÃ³n existentes por niveles 5.1kV-10kV
    inst_5_10_kV = obtener_instrumentos_rango(5.1, 10, 'kV', inst_tension_subset)

    # Obtener instrumentos de tensiÃ³n existentes por niveles 10.1kV-15kV
    inst_10_15_kV = obtener_instrumentos_rango(10.1, 15, 'kV', inst_tension_subset)

    # Obtener instrumentos de tensiÃ³n existentes por niveles 15.1kV-150kV
    inst_15_150_kV = obtener_instrumentos_rango(15.1, 150, 'kV', inst_tension_subset)

    # Obtener instrumentos de tensiÃ³n existentes por niveles 150.1kV-300kV
    inst_150_300_kV = obtener_instrumentos_rango(15.1, 300, 'kV', inst_tension_subset)

    # Obtener instrumentos de tensiÃ³n existentes por niveles mas de 300kV
    inst_301_kV = obtener_instrumentos_rango(300, 1000000, 'kV', inst_tension_subset)

    # Obtener instrumentos del grupo de magnitudes presion en el rango de 0Pa a 50Pa
    inst_0_50_Pa = obtener_instrumentos_rango(0, 50, 'Pa', instrumentos_grupo_presion)

    # Obtener instrumentos del grupo de magnitudes presion en el rango de 1.1kPa a 7KPa
    inst_1_7_kPa = obtener_instrumentos_rango(1, 7, 'kPa', instrumentos_grupo_presion)

    # Obtener instrumentos del grupo de magnitudes presion en el rango de 7.1kPa a 10kPa
    inst_7_10_kPa = obtener_instrumentos_rango(7.1, 10, 'kPa', instrumentos_grupo_presion)

    # Obtener instrumentos del grupo de magnitudes presion en el rango de 10.1kPa a 20kPa
    inst_10_20_kPa = obtener_instrumentos_rango(10.1, 20, 'kPa', instrumentos_grupo_presion)

    # Obtener instrumentos del grupo de magnitudes presion en el rango de 20.1kPa a 25kPa
    inst_20_25_kPa = obtener_instrumentos_rango(20.1, 25, 'kPa', instrumentos_grupo_presion)

    # Obtener instrumentos con nombre micrometro en el rango hasta 100mm
    inst_micrometro_100_mm = obtener_instrumentos_rango(-1000000, 100, 'mm', instr_micrometro)

    # Obtener instrumentos con nombre micrometro en el rango entre  100mm y 500mm
    inst_micrometro_100_500_mm = obtener_instrumentos_rango(100.1, 500, 'mm', instr_micrometro)

    # Obtener instrumentos con nombre micrometro en el rango entre  100mm y 500mm
    inst_micrometro_500_1000_mm = obtener_instrumentos_rango(500.1, 1000, 'mm', instr_micrometro)

    # Obtener instrumentos con nombre micrometro en el rango entre  100mm y 500mm
    inst_micrometro_1000_mm = obtener_instrumentos_rango(1000.1, 1000000, 'mm', instr_micrometro)

    dictionary = cantidad_inst_por_grupo(instr_trab, magns)

    return render(request, 'corp/rng/rango.html',
                  {'cant_trab': cant_trab,
                   'inst_trab_more_info': json.dumps(inst_trab_more_info),

                   'count_vacuometro': count_vacuometro,
                   'inst_vacuometro_more_info': json.dumps(inst_vacuometro_more_info),

                   'count_pie_rey': count_pie_rey,
                   'inst_pie_rey_more_info': json.dumps(inst_pie_rey_more_info),

                   'count_pie_rey_profundidad': count_pie_rey_profundidad,
                   'inst_pie_rey_profundidad_more_info': json.dumps(inst_pie_rey_profundidad_more_info),

                   'count_micrometro': count_micrometro,
                   'inst_micrometro_more_info': json.dumps(inst_micrometro_more_info),

                   'count_cintas': cant_cintas,
                   'inst_cintas_more_info': json.dumps(inst_cintas_more_info),

                   'count_medidor_nivel': cant_medidor_nivel,
                   'inst_medidor_nivel_more_info': json.dumps(inst_medidor_nivel_more_info),

                   'count_medidor_angulo': cant_medidor_angulo,
                   'inst_medidor_angulo_more_info': json.dumps(inst_medidor_angulo_more_info),

                   'count_comparador_caratula': cant_comparador_caratula,
                   'inst_comparador_caraturla_more_info': json.dumps(inst_comparador_caraturla_more_info),

                   'count_regla': cant_regla,
                   'inst_regla_more_info': json.dumps(inst_regla_more_info),

                   'count_galga': cant_galga,
                   'inst_galga_more_info': json.dumps(inst_galga_more_info),

                   'count_ttr': cant_ttr,
                   'inst_ttr_more_info': json.dumps(inst_ttr_more_info),

                   'count_arm': cant_armonico,
                   'inst_armonico_more_info': json.dumps(inst_armonico_more_info),

                   'count_multif': cant_multif,
                   'inst_multif_more_info': json.dumps(inst_multif_more_info),

                   'count_mag_frec': count_mag_frec,
                   'inst_mag_frec_more_info': json.dumps(inst_mag_frec_more_info),

                   'inst_1_kV': inst_1_kV,
                   'inst_1_5_V': inst_1_5_kV,
                   'inst_5_10_kV': inst_5_10_kV,
                   'inst_10_15_kV': inst_10_15_kV,
                   'inst_15_150_kV': inst_15_150_kV,
                   'inst_150_300_kV': inst_150_300_kV,
                   'inst_301_kV': inst_301_kV,
                   'inst_0_50_Pa': inst_0_50_Pa,
                   'inst_1_7_kPa': inst_1_7_kPa,
                   'inst_7_10_kPa': inst_7_10_kPa,
                   'inst_10_20_kPa': inst_10_20_kPa,
                   'inst_20_25_kPa': inst_20_25_kPa,
                   'inst_micrometro_100_mm': inst_micrometro_100_mm,
                   'inst_micrometro_100_500_mm': inst_micrometro_100_500_mm,
                   'inst_micrometro_500_1000_mm': inst_micrometro_500_1000_mm,
                   'inst_micrometro_1000_mm': inst_micrometro_1000_mm,
                   'electr': dictionary.get('elect'),
                   'presion': dictionary.get('presion'),
                   'temp': dictionary.get('temp'),
                   'flujo': dictionary.get('flujo'),
                   'volumen': dictionary.get('volumen'),
                   'dim': dictionary.get('dim'),
                   'masa': dictionary.get('masa'),
                   'fuerza': dictionary.get('fuerza'),
                   'fis_quim': dictionary.get('fis_quim'),
                   'vibr': dictionary.get('vibr'),
                   'ruido': dictionary.get('ruido'),
                   'ilum': dictionary.get('ilum'),
                   'miliohm': miliohm_lista,
                   'ohm': ohm_lista,
                   'kiloohm': kiloohm_lista,
                   'megaohm': megaohm_lista,
                   })


@role_required(allowed_roles=['Ejecutivo', 'Administrador'])
def instrumentos_trabajo_pc(request):
    instr_single = remove_duplicated_instruments()
    inst_trab = []
    for i in instr_single:
        if i.catusonom.catusonom == 'Trabajo':
            inst_trab.append(i)

    # Determinar instrumentos por procesos corporativos

    instruments_per_companies_per_provinces = instrumentos_procesos_corporativos(inst_trab)

    return render(request, 'corp/rng/instr_trab_proc_corp.html', {'ipcpp': instruments_per_companies_per_provinces})


@role_required(allowed_roles=['Ejecutivo', 'Administrador'])
def instrumentos_trabajo_explot(request):
    instr_single = remove_duplicated_instruments()
    inst_trab = []
    for i in instr_single:
        if i.catusonom.catusonom == 'Trabajo':
            inst_trab.append(i)

    # Determinar instrumentos por años de explotacion

    inst_per_comp_0_10, inst_per_comp_10_20, inst_per_comp_20 = instrumentos_anhos_explotacion(inst_trab)

    return render(request, 'corp/rng/instr_trab_explot.html', {'ipcpp_0_10': inst_per_comp_0_10,
                                                               'ipcpp_10_20': inst_per_comp_10_20,
                                                               'ipcpp_20': inst_per_comp_20})


@role_required(allowed_roles=['Ejecutivo', 'Administrador'])
def instrumentos_trabajo_fabr(request):
    instr_single = remove_duplicated_instruments()
    inst_trab = []
    for i in instr_single:
        if i.catusonom.catusonom == 'Trabajo':
            inst_trab.append(i)

    # Determinar instrumentos por fabricante

    list1, list2, list3, list4 = obtener_instrumento_fabricante(inst_trab)

    return render(request, 'corp/rng/instr_trab_fabr.html', {'fab1': list1,
                                                             'fab2': list2,
                                                             'fab3': list3,
                                                             'fab4': list4})


@role_required(allowed_roles=['Ejecutivo', 'Administrador'])
def patrones(request):
    # Determinar cantidad de instrumentos que sean patrones

    instr_single = remove_duplicated_instruments()
    instr_patr = []

    cant_patr = 0
    inst_patr_more_info = dict()

    cant_energia_monofasico = 0
    inst_energia_monofasico_more_info = dict()

    cant_energia_trifasico = 0
    inst_energia_trifasico_more_info = dict()

    cant_patr_ener_trab = 0
    inst_patr_ener_trab_more_info = dict()

    cant_rel_trans = 0
    inst_rel_trans = dict()

    cant_patr_metalograficos = 0
    inst_patr_metalograficos_more_info = dict()

    cant_patr_quimicos = 0
    inst_patr_quimicos_more_info = dict()

    for isin in instr_single:
        if isin.catusonom.catusonom == 'Patrón':
            instr_patr.append(isin)
            cant_patr += 1
            inst_patr_more_info = more_info(isin, inst_patr_more_info)

    # Determinar la cantidad de instrumentos patrones de energia monofasicos

    cad = "Patrón de energía monofásicos de alta exactitud"
    cad1 = "Patrón de energía monofasicos de alta exactitud"
    cad2 = "Patrón de energia monofásicos de alta exactitud"
    cad3 = "Patrón de energia monofasicos de alta exactitud"
    for ip in instr_patr:
        desc = str(ip.instdescripcion).lower()
        if desc == cad.lower() or desc == cad1.lower() or desc == cad2.lower() or desc == cad3.lower():
            cant_energia_monofasico += 1
            inst_energia_monofasico_more_info = more_info(ip, inst_energia_monofasico_more_info)
    # Determinar la cantidad de instrumentos patrones de energia trifasicos

    cad = "Patrón de energía trifásicos de alta exactitud"
    cad1 = "Patrón de energía trifasicos de alta exactitud"
    cad2 = "Patrón de energia trifásicos de alta exactitud"
    cad3 = "Patrón de energia trifasicos de alta exactitud"
    for ip in instr_patr:
        desc = str(ip.instdescripcion).lower()
        if desc == cad.lower() or desc == cad1.lower() or desc == cad2.lower() or desc == cad3.lower():
            cant_energia_trifasico += 1
            inst_energia_trifasico_more_info = more_info(ip, inst_energia_trifasico_more_info)
    # Determinar la cantidad de instrumentos patrones de energia de trabajo

    cad1 = 'Patrón de energia de trabajo'
    cad2 = 'Patrón de energía de trabajo'
    for ip in instr_patr:
        if str(ip.instdescripcion).lower() == cad1.lower() or str(ip.instdescripcion).lower() == cad2.lower():
            cant_patr_ener_trab += 1
            inst_patr_ener_trab_more_info = more_info(ip, inst_patr_ener_trab_more_info)
    # Determinar la cantidad de instrumentos patrones de trabajo

    # Determinar cantidad de patrones de electricidad
    magnitudes = remove_duplicated_magnitudes()

    dictionary = cantidad_inst_por_grupo(instr_patr, magnitudes)

    instr_patr_elect = dictionary.get('inst_elect')
    instr_patr_pres = dictionary.get('inst_presion')
    instr_patr_temp = dictionary.get('inst_tmp')

    cant_electr_intensidad, cant_electr_tension, cant_electr_resistencia = cantidad_patrones_por_magnitud(
        instr_patr_elect, magnitudes)

    # Determinar cantidad de patrones de relacion de Transformacion

    cad = "Medidor de Relación de Transformación"
    cad1 = "TTR"
    for ip in instr_patr:
        if str(ip.instdescripcion).lower() == cad.lower() or str(ip.instdescripcion).lower() == cad1.lower():
            cant_rel_trans += 1
            inst_rel_trans = more_info(ip, inst_rel_trans)
    # Determinar cantidad de patrones de presion hasta 1MPa
    presion_1mpa = obtener_instrumentos_rango(-1000000, 1, 'MPa', instr_patr_pres)

    # Determinar cantidad de patrones de presion hasta 1.1MPa a 10MPa
    presion_1_10 = obtener_instrumentos_rango(1.1, 10, 'MPa', instr_patr_pres)

    # Determinar cantidad de patrones de presion hasta 10.1MPa a 100MPa
    presion_10_100 = obtener_instrumentos_rango(10.1, 100, 'MPa', instr_patr_pres)

    # Determinar cantidad de patrones de presion hasta 100.1MPa a 250MPa
    presion_100_250 = obtener_instrumentos_rango(100.1, 250, 'MPa', instr_patr_pres)

    # Determinar cantidad de patrones de temperatura hasta 100 grados
    temp_100 = obtener_instrumentos_rango(-1000000, 100, 'ÂºC', instr_patr_temp)

    # Determinar cantidad de patrones de temperatura de 100 grados a 500grados
    temp_100_500 = obtener_instrumentos_rango(100.1, 500, 'ÂºC', instr_patr_temp)

    # Determinar cantidad de patrones de temperatura de 500grados a 1000grados
    temp_500_1000 = obtener_instrumentos_rango(500.1, 1000, 'ÂºC', instr_patr_temp)

    # Determinar cantidad de patrones de temperatura de 1000grados a 2000grados
    temp_1000_2000 = obtener_instrumentos_rango(1000.1, 2000, 'ÂºC', instr_patr_temp)

    # Determinar cantidad de patrones de ensayos metalograficos

    cad = "Patrón de ensayos metalográficos"
    cad1 = "Patrón de ensayos metalograficos"
    for ip in instr_patr:
        if str(ip.instdescripcion).lower() == cad.lower() or str(ip.instdescripcion).lower() == cad1.lower():
            cant_patr_metalograficos += 1
            inst_patr_metalograficos_more_info = more_info(ip, inst_patr_metalograficos_more_info)
    # Determinar cantidad de patrones de ensayos quimicos

    cad = "Patrón de ensayos químicos"
    cad1 = "Patrón de ensayos quimicos"
    for ip in instr_patr:
        if str(ip.instdescripcion).lower() == cad.lower() or str(ip.instdescripcion).lower() == cad1.lower():
            cant_patr_quimicos += 1
            inst_patr_quimicos_more_info = more_info(ip, inst_patr_quimicos_more_info)

    return render(request, 'corp/patron/patron.html', {'cant_patr': cant_patr,
                                                       'inst_patr_more_info': json.dumps(inst_patr_more_info),
                                                       'cant_energia_monofasico': cant_energia_monofasico,
                                                       'inst_energia_monofasico_more_info': json.dumps(
                                                           inst_energia_monofasico_more_info),
                                                       'cant_energia_trifasico': cant_energia_trifasico,
                                                       'inst_energia_trifasico_more_info': json.dumps(
                                                           inst_energia_trifasico_more_info),
                                                       'cant_patr_ener_trab': cant_patr_ener_trab,
                                                       'inst_patr_ener_trab_more_info': json.dumps(
                                                           inst_patr_ener_trab_more_info),
                                                       'electr': dictionary.get('elect'),
                                                       'cant_electr_intensidad': cant_electr_intensidad,
                                                       'cant_electr_tension': cant_electr_tension,
                                                       'cant_electr_resistencia': cant_electr_resistencia,

                                                       'cant_rel_trans': cant_rel_trans,
                                                       'inst_rel_trans': json.dumps(inst_rel_trans),

                                                       'presion': dictionary.get('presion'),
                                                       'presion_1mpa': presion_1mpa,
                                                       'presion_1_10': presion_1_10,
                                                       'presion_10_100': presion_10_100,
                                                       'presion_100_250': presion_100_250,
                                                       'temp': dictionary.get('temp'),
                                                       'temp_100': temp_100,
                                                       'temp_100_500': temp_100_500,
                                                       'temp_500_1000': temp_500_1000,
                                                       'temp_1000_2000': temp_1000_2000,
                                                       'patr_dimensional': dictionary.get('cant_dim'),
                                                       'patr_dureza': dictionary.get('dureza'),

                                                       'cant_patr_metalografico': cant_patr_metalograficos,
                                                       # New
                                                       'inst_patr_metalograficos_more_info': inst_patr_metalograficos_more_info,

                                                       'cant_patr_quimicos': cant_patr_quimicos,
                                                       'inst_patr_quimicos_more_info': inst_patr_quimicos_more_info,

                                                       'flujo': dictionary.get('flujo'),
                                                       'volumen': dictionary.get('volumen'),
                                                       'masa': dictionary.get('masa'),
                                                       'fuerza': dictionary.get('fuerza'),
                                                       'fis_quim': dictionary.get('fis_quim'),
                                                       'vibr': dictionary.get('vibr'),
                                                       'ruido': dictionary.get('ruido'),
                                                       'ilum': dictionary.get('ilum'),
                                                       })


@role_required(allowed_roles=['Ejecutivo', "Administrador"])
def informe_magnitudes(request):
    export_informe_magnitudes()

    filename = 'Informe Instrumentos.xlsx'
    # Define the full file path
    file_path = 'static/docs/' + filename
    # Open the file for reading content

    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
