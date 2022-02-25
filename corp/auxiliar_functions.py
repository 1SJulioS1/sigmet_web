from datetime import date

import pandas as pd
import xlsxwriter
import json

from corp.models import *


def obtener_instrumentos_rango(minimo, maximo, unidad_de_medicion, instrument_subset):
    if instrument_subset == "":
        instrument_subset = Instrumentos.objects.all()
    rel = Relacionmagnitudesunidadesmedicion.objects.all()
    caract_met = Caracteristicasmetrologicas.objects.all()
    try:
        unimed = Unidadesmedicion.objects.filter(unimedsim=unidad_de_medicion)
        rango = Rangosmedicion.objects.all()
        count = 0
        for um in unimed:
            for r in rel:
                if r.idunimed_id == um.idunimed and r.unimediddb_id == um.unimediddb:
                    for ra in rango:
                        if ra.idrelmagunimed_id == r.idrelmagunimed and \
                                ra.relmagunimediddb_id == r.relmagunimediddb and \
                                float(ra.rngmedlimsup) <= float(maximo) and \
                                float(ra.rngmedliminf) >= float(minimo):
                            for cm in caract_met:
                                if cm.idrngmed_id == ra.idrngmed and cm.rngmediddb_id == ra.rngmediddb:
                                    for i in instrument_subset:
                                        if cm.idinst_id == i.idinst:
                                            count += 1
                                            break
    except Unidadesmedicion.DoesNotExist:
        count = 0

    return count


def instrumentos_por_magnitud():
    grupo = Gruposmagnitudes.objects.all()
    magns = Magnitudes.objects.all()
    instr_single = remove_duplicated_instruments()

    inst_per_mag_per_group = dict()
    for g in grupo:
        inst_per_magns = dict()
        for m in magns:
            if m.grpmagnom.grpmagnom == g.grpmagnom:
                count = 0
                inst_per_comp = dict()
                for i in instr_single:
                    if i.idmag_id == m.idmag and i.magiddb_id == m.magiddb:
                        count += 1
                        inst_per_comp = more_info(i, inst_per_comp)
                aux = dict()
                aux[str(count)] = json.dumps(inst_per_comp)
                inst_per_magns[m.magnom] = aux
        inst_per_mag_per_group[g.grpmagnom] = inst_per_magns

    return inst_per_mag_per_group


def cantidad_inst_por_grupo(instr_patr, magnitudes):
    instr_patr_elect = []
    cant_elect = 0
    instr_patr_pres = []
    cant_presion = 0
    instr_patr_temp = []
    cant_temp = 0
    cant_flujo = 0
    cant_volumen = 0
    cant_dim = 0
    cant_masa = 0
    cant_fuerza = 0
    cant_fis_quim = 0
    cant_dureza = 0
    cant_vibr = 0
    cant_ruido = 0
    cant_ilum = 0

    for ip in instr_patr:
        for me in magnitudes:
            if ip.idmag_id == me.idmag and ip.magiddb_id == me.magiddb:
                if str(me.grpmagnom.grpmagnom).lower() == 'electricidad':
                    cant_elect += 1
                    instr_patr_elect.append(ip)
                else:
                    if str(me.grpmagnom.grpmagnom).lower() == 'presión':
                        cant_presion += 1
                        instr_patr_pres.append(ip)
                    else:
                        if str(me.grpmagnom.grpmagnom).lower() == 'temperatura':
                            cant_temp += 1
                            instr_patr_temp.append(ip)
                        else:
                            if str(me.grpmagnom.grpmagnom).lower() == 'dimensional':
                                cant_dim += 1
                            else:
                                if str(me.grpmagnom.grpmagnom).lower() == 'dureza':
                                    cant_dureza += 1
                                else:
                                    if str(me.grpmagnom.grpmagnom).lower() == 'flujo/gasto' or \
                                            str(me.grpmagnom.grpmagnom).lower() == 'flujo' or \
                                            str(me.grpmagnom.grpmagnom).lower() == 'gasto':
                                        cant_flujo += 1
                                    else:
                                        if str(me.grpmagnom.grpmagnom).lower() == 'volumen' or \
                                                str(me.grpmagnom.grpmagnom).lower() == 'volúmen':
                                            cant_volumen += 1
                                        else:
                                            if str(me.grpmagnom.grpmagnom).lower() == 'masa':
                                                cant_masa += 1
                                            else:
                                                if str(me.grpmagnom.grpmagnom).lower().__contains__('fuerza'):
                                                    cant_fuerza += 1
                                                else:
                                                    if str(me.grpmagnom.grpmagnom).lower() == 'vibraciones' or \
                                                            str(me.grpmagnom.grpmagnom).lower() == 'vibración' or \
                                                            str(me.grpmagnom.grpmagnom).lower() == 'vibracion':
                                                        cant_vibr += 1
                                                    else:
                                                        if str(me.grpmagnom.grpmagnom).lower() == 'fisico-quimico' or \
                                                                str(me.grpmagnom.grpmagnom).lower() == 'físico-químico':
                                                            cant_fis_quim += 1
                                                        else:
                                                            if str(
                                                                    me.grpmagnom.grpmagnom).lower() == 'ruidos-sonometros' or \
                                                                    str(
                                                                        me.grpmagnom.grpmagnom).lower() == 'ruidos-sonómetros':
                                                                cant_ruido += 1
                                                            else:
                                                                if str(
                                                                        me.grpmagnom.grpmagnom).lower() == 'iluminacion-luxometros' or \
                                                                        str(
                                                                            me.grpmagnom.grpmagnom).lower() == 'iluminación-luxómetros' or \
                                                                        str(
                                                                            me.grpmagnom.grpmagnom).lower() == 'iluminacion-luxómetros' or \
                                                                        str(
                                                                            me.grpmagnom.grpmagnom).lower() == 'iluminación-luxometros':
                                                                    cant_ilum += 1

    dictionary = {
        'instr_patr_elect': instr_patr_elect,
        'cant_elect': cant_elect,
        'instr_patr_pres': instr_patr_pres,
        'cant_presion': cant_presion,
        'instr_patr_temp': instr_patr_temp,
        'cant_temp': cant_temp,
        'cant_flujo': cant_flujo,
        'cant_volumen': cant_volumen,
        'cant_dim': cant_dim,
        'cant_masa': cant_masa,
        'cant_fuerza': cant_fuerza,
        'cant_fis_quim': cant_fis_quim,
        'cant_dureza': cant_dureza,
        'cant_vibr': cant_vibr,
        'cant_ruido': cant_ruido,
        'cant_ilum': cant_ilum,
    }

    return dictionary


def cantidad_patrones_por_magnitud(instr_patr, magnitudes):
    int_elec = 0
    ten_elec = 0
    res_elec = 0

    for ip in instr_patr:
        for me in magnitudes:
            if ip.idmag_id == me.idmag and ip.magiddb_id == me.magiddb:
                if me.magnom == 'Intensidad de corriente eléctrica':
                    int_elec += 1
                    break
                else:
                    if me.magnom == 'Tensión eléctrica':
                        ten_elec += 1
                        break
                    else:
                        if me.magnom == 'Resistencia Eléctrica':
                            res_elec += 1
                            break
    return int_elec, ten_elec, res_elec


def remove_duplicated_instruments():
    instrumentos = Instrumentos.objects.all()
    instr_single = []
    flag = 0
    for i in instrumentos:
        for ip in instr_single:
            if ip.instnom == i.instnom and ip.instmarca == i.instmarca and ip.instmodelo == i.instmodelo and \
                    ip.instnoserie == i.instnoserie and ip.instnoinv == i.instnoinv and ip.instanhofab == i.instanhofab and \
                    ip.catusonom.catusonom == i.catusonom.catusonom and ip.catinstnom.catinstnom == i.catinstnom.catinstnom:
                flag = 1
                break
        if flag == 0:
            instr_single.append(i)
        flag = 0
    return instr_single


def remove_duplicated_campanies():
    emp = Empresas.objects.all()
    emp_single = []
    flag = 0
    for e in emp:
        for es in emp_single:
            if es.empnom == e.empnom and es.empnomcom == e.empnomcom:
                flag = 1
                break
        if flag == 0:
            emp_single.append(e)
        flag = 0
    return emp_single


def obtener_instrumento_fabricante(instr):
    inst_fabr = dict()
    for i in instr:
        inst_fabr[i.instmarca] = 0
    for marca in inst_fabr:
        inst_gen = dict()
        contador = 0
        for i in instr:
            if i.instmarca == marca:
                contador += 1
                inst_gen = more_info(i, inst_gen)
        aux = {
            contador: inst_gen
        }
        inst_fabr[marca] = aux
    count = inst_fabr.__len__()

    list1 = []
    list2 = []
    list3 = []
    list4 = []
    count1 = count / 4
    count2 = 0
    for item in inst_fabr:
        new_dict = inst_fabr[item]
        for item2 in new_dict:
            if count2 < count1:
                list1.append((item, item2, json.dumps(new_dict[item2])))
            else:
                if count2 < count1 * 2:
                    list2.append((item, item2, json.dumps(new_dict[item2])))
                else:
                    if count2 < count1 * 3:
                        list3.append((item, item2, json.dumps(new_dict[item2])))
                    else:
                        if count2 < count1 * 4:
                            list4.append((item, item2, json.dumps(new_dict[item2])))
        count2 += 1

    return list1, list2, list3, list4


def instrumentos_medidores_resistencia(instr_single):
    unimed = Unidadesmedicion.objects.all()
    relmagunimed = Relacionmagnitudesunidadesmedicion.objects.all()
    rangos = Rangosmedicion.objects.all()
    caractmet = Caracteristicasmetrologicas.objects.all()

    miliohm = dict()
    ohm = dict()
    kiloohm = dict()
    megaohm = dict()

    miliohm_lista = []
    ohm_lista = []
    kiloohm_lista = []
    megaohm_lista = []

    count_miliohm = 0
    count_ohm = 0
    count_kiloohm = 0
    count_megaohm = 0
    for um in unimed:
        if um.unimednom == 'Miliohm' or um.unimednom == 'miliohm':
            for rmu in relmagunimed:
                if rmu.idunimed_id == um.idunimed and rmu.unimediddb_id == um.unimediddb:
                    for rng in rangos:
                        if rng.idrelmagunimed_id == rmu.idrelmagunimed and \
                                rng.relmagunimediddb_id == rmu.relmagunimediddb:
                            cadena = 'De ' + str(float(rng.rngmedliminf)) + ' a ' + str(float(rng.rngmedlimsup))
                            for cm in caractmet:
                                if cm.idrngmed_id == rng.idrngmed and cm.rngmediddb_id == rng.rngmediddb:
                                    for ins in instr_single:
                                        if ins.idinst == cm.idinst_id:
                                            count_miliohm += 1
                            if count_miliohm != 0:
                                if cadena in miliohm:
                                    miliohm[cadena] += count_miliohm
                                else:
                                    miliohm[cadena] = count_miliohm
                            count_miliohm = 0
        else:
            if um.unimednom == 'Ohm' or um.unimednom == 'ohm':
                for rmu in relmagunimed:
                    if rmu.idunimed_id == um.idunimed and rmu.unimediddb_id == um.unimediddb:
                        for rng in rangos:
                            if rng.idrelmagunimed_id == rmu.idrelmagunimed and \
                                    rng.relmagunimediddb_id == rmu.relmagunimediddb:
                                cadena = 'De ' + str(float(rng.rngmedliminf)) + ' a ' + str(float(rng.rngmedlimsup))
                                for cm in caractmet:
                                    if cm.idrngmed_id == rng.idrngmed and cm.rngmediddb_id == rng.rngmediddb:
                                        for ins in instr_single:
                                            if ins.idinst == cm.idinst_id:
                                                count_ohm += 1
                                if count_ohm != 0:
                                    if cadena in miliohm:
                                        ohm[cadena] += count_ohm
                                    else:
                                        ohm[cadena] = count_ohm
                                count_ohm = 0
            else:
                if um.unimednom == 'Kiloohm' or um.unimednom == 'kiloohm':
                    for rmu in relmagunimed:
                        if rmu.idunimed_id == um.idunimed and rmu.unimediddb_id == um.unimediddb:
                            for rng in rangos:
                                if rng.idrelmagunimed_id == rmu.idrelmagunimed and \
                                        rng.relmagunimediddb_id == rmu.relmagunimediddb:
                                    cadena = 'De ' + str(float(rng.rngmedliminf)) + ' a ' + \
                                             str(float(rng.rngmedlimsup))
                                    for cm in caractmet:
                                        if cm.idrngmed_id == rng.idrngmed and cm.rngmediddb_id == rng.rngmediddb:
                                            for ins in instr_single:
                                                if ins.idinst == cm.idinst_id:
                                                    count_kiloohm += 1
                                    if count_kiloohm != 0:
                                        if cadena in kiloohm:
                                            kiloohm[cadena] += count_kiloohm
                                        else:
                                            kiloohm[cadena] = count_kiloohm
                                    count_kiloohm = 0
                else:
                    if um.unimednom == 'Megaohm' or um.unimednom == 'megaohm':
                        for rmu in relmagunimed:
                            if rmu.idunimed_id == um.idunimed and rmu.unimediddb_id == um.unimediddb:
                                for rng in rangos:
                                    if rng.idrelmagunimed_id == rmu.idrelmagunimed and \
                                            rng.relmagunimediddb_id == rmu.relmagunimediddb:
                                        cadena = 'De ' + str(float(rng.rngmedliminf)) + ' a ' + \
                                                 str(float(rng.rngmedlimsup))
                                        for cm in caractmet:
                                            if cm.idrngmed_id == rng.idrngmed and cm.rngmediddb_id == rng.rngmediddb:
                                                for ins in instr_single:
                                                    if ins.idinst == cm.idinst_id:
                                                        count_megaohm += 1
                                        if count_megaohm != 0:
                                            if cadena in miliohm:
                                                megaohm[cadena] += count_megaohm
                                            else:
                                                megaohm[cadena] = count_megaohm
                                        count_megaohm = 0
    keys_miliohm = miliohm.keys()
    keys_ohm = ohm.keys()
    keys_kilohm = kiloohm.keys()
    keys_megaohm = megaohm.keys()
    for k in keys_miliohm:
        miliohm_lista.append((k, miliohm[k]))
    for k in keys_ohm:
        ohm_lista.append((k, ohm[k]))
    for k in keys_kilohm:
        kiloohm_lista.append((k, kiloohm[k]))
    for k in keys_megaohm:
        megaohm_lista.append((k, megaohm[k]))

    return miliohm_lista, ohm_lista, kiloohm_lista, megaohm_lista


def instrumentos_procesos_corporativos(instr_single):
    emp_single = remove_duplicated_campanies()
    relatribproc = Relacionatributosprocesos.objects.all()
    prov = Provincias.objects.all()
    count = 0
    list_of_proccorp = dict()
    auxiliar = []
    instruments_per_companies = []
    instruments_per_companies_per_provinces = []
    for p in prov:
        for es in emp_single:
            if es.idmun.idprov.idprov == p.idprov:
                for rel in relatribproc:
                    for inst in instr_single:
                        if inst.idemp_id == es.idemp and inst.idrelatribproccorp_id == rel.idrelatribproccorp and \
                                inst.relatribprociddb_id == rel.relatribprociddb:
                            count += 1
                    if count != 0:
                        if rel.proccorpnom.proccorpnom in list_of_proccorp:
                            list_of_proccorp[rel.proccorpnom.proccorpnom] += count
                        else:
                            list_of_proccorp[rel.proccorpnom.proccorpnom] = count
                        count = 0
                keys = list_of_proccorp.keys()
                for k in keys:
                    auxiliar.append((k, list_of_proccorp[k]))
                instruments_per_companies.append((es.empnom, auxiliar))
                list_of_proccorp = dict()
                auxiliar = []
        instruments_per_companies_per_provinces.append((p.provnom, instruments_per_companies))
        instruments_per_companies = []

    return instruments_per_companies_per_provinces


def instrumentos_anhos_explotacion(instr_single):
    prov = Provincias.objects.all()
    emp_single = remove_duplicated_campanies()
    inst_may_20_anhos = dict()
    inst_entre_10_20_anhos = dict()
    inst_0_10_anhos = dict()
    actual_date = date.today()
    inst_per_comp_0_10 = []
    inst_per_comp_10_20 = []
    inst_per_comp_20 = []

    for p in prov:
        for es in emp_single:
            if es.idmun.idprov.idprov == p.idprov:
                for ins in instr_single:
                    if ins.catusonom.catusonom == 'Trabajo':
                        if ins.idemp_id == es.idemp:
                            if ins.instfechapuestoserv is not None:
                                if ins.instfechapuestoserv.year < actual_date.year - 20:
                                    if es.empnom in inst_may_20_anhos:
                                        inst_may_20_anhos[es.empnom] += 1
                                    else:
                                        inst_may_20_anhos[es.empnom] = 1
                                else:
                                    if actual_date.year - 10 > ins.instfechapuestoserv.year >= actual_date.year - 20:
                                        if es.empnom in inst_entre_10_20_anhos:
                                            inst_entre_10_20_anhos[es.empnom] += 1
                                        else:
                                            inst_entre_10_20_anhos[es.empnom] = 1
                                    else:
                                        if actual_date.year - 10 < ins.instfechapuestoserv.year:
                                            if es.empnom in inst_0_10_anhos:
                                                inst_0_10_anhos[es.empnom] += 1
                                            else:
                                                inst_0_10_anhos[es.empnom] = 1
        keys1 = inst_may_20_anhos.keys()
        keys2 = inst_entre_10_20_anhos.keys()
        keys3 = inst_0_10_anhos.keys()
        auxiliar1 = []
        auxiliar2 = []
        auxiliar3 = []
        for k in keys1:
            auxiliar1.append((k, inst_may_20_anhos[k]))
        for k in keys2:
            auxiliar2.append((k, inst_entre_10_20_anhos[k]))
        for k in keys3:
            auxiliar3.append((k, inst_0_10_anhos[k]))
        inst_per_comp_0_10.append((p.provnom, auxiliar3))
        inst_per_comp_10_20.append((p.provnom, auxiliar2))
        inst_per_comp_20.append((p.provnom, auxiliar1))
        inst_0_10_anhos = dict()
        inst_entre_10_20_anhos = dict()
        inst_may_20_anhos = dict()

    return inst_per_comp_0_10, inst_per_comp_10_20, inst_per_comp_20


def magnitudes_por_provincias():
    df = pd.read_excel('static/docs/Arruza- Tabla Levantamiento magnitudes.xlsx', sheet_name=None)
    sheets = list(df.keys())
    del sheets[0]
    del sheets[len(sheets) - 2:len(sheets)]
    columns = []
    for i in range(0, len(sheets)):
        columns.append('B')
    p = {}
    for ws, c in zip(sheets, columns):
        p[ws] = pd.read_excel('static/docs/Arruza- Tabla Levantamiento magnitudes.xlsx', sheet_name=ws, usecols=c)

    magnitud_denominacion = {}
    for i in p.keys():
        r = p[i].dropna().drop([0]).values
        magnitud_denominacion[i] = r

    instr_single = remove_duplicated_instruments()  # elimino los instrumentos repetidos
    emp_single = remove_duplicated_campanies()  # elimino las empresas repetidas
    prov = Provincias.objects.all()
    caract_met = Caracteristicasmetrologicas.objects.all()
    rangos = Rangosmedicion.objects.all()
    magn = Magnitudes.objects.all()
    rel = Relacionmagnitudesunidadesmedicion.objects.all()

    inst_per_prov_per_magn = []

    for k in magnitud_denominacion.keys():
        inst_per_prov = []
        for denom in magnitud_denominacion[k]:
            denom_inst = str(denom.tolist()[0])
            nombre = denom_inst.lower()
            lista = [-1]
            unidad_medicion = ''
            exactitud = [-1]
            if nombre == 'micrómetro para exteriores':
                lista = [200, 1000000]
                unidad_medicion = 'mm'
            else:
                if nombre == 'pie de rey de exteriores' or \
                        nombre == 'pie de rey de interiores y exteriores' or \
                        nombre == 'pie de rey universal' or \
                        nombre == 'pie de rey de profundidad' or \
                        nombre == 'pie de rey de altura':
                    lista = [200, 1000, 1000000]
                    unidad_medicion = 'mm'
                else:
                    if nombre == 'indicador de esfera':
                        lista = [10, 1000000]
                        unidad_medicion = 'mm'
                    else:
                        if nombre == 'escuadra cilíndirca':
                            lista = [200]
                            unidad_medicion = 'mm'
                        else:
                            if nombre == 'escala de vidrio':
                                lista = [50, 100, 200]
                                unidad_medicion = 'mm'
                            else:
                                if nombre == 'escuadra':
                                    lista = [400, 1000000]
                                    unidad_medicion = 'mm'
                                else:
                                    if nombre == 'mármol':
                                        lista = [1000, 1000000]
                                        unidad_medicion = 'mm'
                                    else:
                                        if nombre == 'máquina de medición de 1-D':
                                            lista = [1000]
                                            unidad_medicion = 'mm'
                                        else:
                                            if nombre == 'pesa clase f2':
                                                lista = [500]
                                                unidad_medicion = 'g'
                                            else:
                                                if nombre == 'pesa clase m1-m3':
                                                    lista = [5, 10, 20, 50]
                                                    unidad_medicion = 'kg'
                                                else:
                                                    if nombre == 'pesa':
                                                        lista = [500, 1000]
                                                        unidad_medicion = 'kg'
                                                    else:
                                                        if nombre == 'instrumento de pesar no automático':
                                                            lista = [1, 200, 1000, 10000, 1000000]
                                                            unidad_medicion = 'kg'
                                                        else:
                                                            if nombre == 'gancho de pesar':
                                                                lista = [200, 5000, 1000000]
                                                                unidad_medicion = 'kg'
                                                            else:
                                                                if nombre == 'microbureta':
                                                                    lista = [5]
                                                                    unidad_medicion = 'cm3'
                                                                else:
                                                                    if nombre == 'bureta':
                                                                        lista = [10, 100]
                                                                        unidad_medicion = 'cm3'
                                                                    else:
                                                                        if nombre == 'recipiente patrón':
                                                                            lista = [20, 200, 1000000]
                                                                            unidad_medicion = 'L'
                                                                        else:
                                                                            if nombre == 'medida técnica':
                                                                                lista = [20, 100, 1000000]
                                                                                unidad_medicion = 'L'
                                                                            else:
                                                                                if nombre == 'tanque de almacenamiento sobre suelo (vertical)':
                                                                                    lista = [50, 2000, 30000, 1000000]
                                                                                    unidad_medicion = 'm3'
                                                                                else:
                                                                                    if nombre == 'tanque de almacenamiento sobre suelo (horizontal)':
                                                                                        lista = [5, 10, 50, 1000000]
                                                                                        unidad_medicion = 'm3'
                                                                                    else:
                                                                                        if nombre == 'tanque de almacenamiento aéreo' or \
                                                                                                nombre == 'tanque de almacenamiento soterrado':
                                                                                            lista = [10, 30, 1000000]
                                                                                            unidad_medicion = 'm3'
                                                                                        else:
                                                                                            if nombre == 'termómetro líquido en vidrio con contacto eléctrico':
                                                                                                lista = [100, 300, 600]
                                                                                                unidad_medicion = '°C'
                                                                                            else:
                                                                                                if nombre == 'termómetro manométrico indicador':
                                                                                                    lista = [100, 300,
                                                                                                             600]
                                                                                                    unidad_medicion = '°C'
                                                                                                else:
                                                                                                    if nombre == 'termómetro manométrico de registro y control':
                                                                                                        lista = [100,
                                                                                                                 300,
                                                                                                                 600]
                                                                                                        unidad_medicion = '°C'
                                                                                                    else:
                                                                                                        if nombre == 'pirómetro óptico':
                                                                                                            lista = [
                                                                                                                2600]
                                                                                                            unidad_medicion = '°C'
                                                                                                        else:
                                                                                                            if nombre == 'pirómetro de radiación':
                                                                                                                lista = [
                                                                                                                    2000]
                                                                                                                unidad_medicion = '°C'
                                                                                                            else:
                                                                                                                if nombre == 'pirómetro infrarrojo':
                                                                                                                    lista = [
                                                                                                                        1500]
                                                                                                                    unidad_medicion = '°C'
                                                                                                                else:
                                                                                                                    if nombre == 'contador de agua doméstico':
                                                                                                                        lista = [
                                                                                                                            5]
                                                                                                                        unidad_medicion = 'm3/h'
                                                                                                                    else:
                                                                                                                        if nombre == 'contador de líquido':
                                                                                                                            lista = [
                                                                                                                                10,
                                                                                                                                60,
                                                                                                                                1000000]
                                                                                                                            unidad_medicion = 'm3/h'
                                                                                                                        else:
                                                                                                                            if nombre == 'cinta de medición':
                                                                                                                                lista = [
                                                                                                                                    5,
                                                                                                                                    20,
                                                                                                                                    50,
                                                                                                                                    1000000]
                                                                                                                                unidad_medicion = 'm'
                                                                                                                            else:
                                                                                                                                if nombre == 'cinta métrica con plomada':
                                                                                                                                    lista = [
                                                                                                                                        30]
                                                                                                                                    unidad_medicion = 'm'
                                                                                                                                else:
                                                                                                                                    if nombre == 'bloque patrón':
                                                                                                                                        lista = [
                                                                                                                                            100,
                                                                                                                                            500,
                                                                                                                                            1000]
                                                                                                                                        exactitud = [
                                                                                                                                            0,
                                                                                                                                            1,
                                                                                                                                            2]
                                                                                                                                        unidad_medicion = 'mm'
                                                                                                                                    else:
                                                                                                                                        if nombre == 'cristal plano inferior' or \
                                                                                                                                                nombre == 'medida angular prismática' or \
                                                                                                                                                nombre == 'dinamómetro ordinario':
                                                                                                                                            exactitud = [
                                                                                                                                                1,
                                                                                                                                                2]
                                                                                                                                        else:
                                                                                                                                            if nombre == 'dinamómetro portátil patrón' or \
                                                                                                                                                    nombre == 'dinamómetro universal patrón' or \
                                                                                                                                                    nombre.__contains__(
                                                                                                                                                        'ómetro de deformación elástica') or \
                                                                                                                                                    nombre == 'manómetro' or nombre == 'vacuómetro':
                                                                                                                                                exactitud = [
                                                                                                                                                    0.5]
                                                                                                                                            else:
                                                                                                                                                if nombre == 'manómetro de líquido' or \
                                                                                                                                                        nombre == 'manómetro de tubo en U' or \
                                                                                                                                                        nombre == 'manómetro de tubo y recipiente' or \
                                                                                                                                                        nombre == 'vacuómetro de líquido' or \
                                                                                                                                                        nombre == 'vacuómetro de tubo en U' or \
                                                                                                                                                        nombre == 'vacuómetro de tubo y recipiente':
                                                                                                                                                    exactitud = [
                                                                                                                                                        0.5,
                                                                                                                                                        1000000]
                                                                                                                                                else:
                                                                                                                                                    if nombre == 'camión cisterna':
                                                                                                                                                        lista = [
                                                                                                                                                            5]
                                                                                                                                                        unidad_medicion = 'm3'
                                                                                                                                                    else:
                                                                                                                                                        if nombre.__contains__(
                                                                                                                                                                'medidor de corriente eléctrica') or \
                                                                                                                                                                nombre.__contains__(
                                                                                                                                                                    'medidor de tensión eléctrica') or \
                                                                                                                                                                nombre.__contains__(
                                                                                                                                                                    'medidor de potencia eléctrica'):
                                                                                                                                                            if nombre.__contains__(
                                                                                                                                                                    'digital') or nombre.__contains__(
                                                                                                                                                                    'analógic'):
                                                                                                                                                                exactitud = [
                                                                                                                                                                    1.0]
                                                                                                                                                            else:
                                                                                                                                                                exactitud = [
                                                                                                                                                                    0.5]
                                                                                                                                                        else:
                                                                                                                                                            if nombre == 'medida con trazos rígida':
                                                                                                                                                                lista = [
                                                                                                                                                                    1]
                                                                                                                                                                unidad_medicion = 'm'
                                                                                                                                                            else:
                                                                                                                                                                if nombre == 'regla':
                                                                                                                                                                    lista = [
                                                                                                                                                                        1000,
                                                                                                                                                                        1000000]
                                                                                                                                                                    exactitud = [
                                                                                                                                                                        1,
                                                                                                                                                                        1000000]
                                                                                                                                                                    unidad_medicion = 'mm'

            if unidad_medicion != '':
                unimed = Unidadesmedicion.objects.filter(unimedsim=unidad_medicion)
            else:
                unimed = []
            count_exact = -1
            for exact in exactitud:
                count_exact += 1
                count = -1
                for valor in lista:
                    count += 1
                    dict_ctd_inst = dict()
                    for p in prov:
                        count_prov = 0
                        for es in emp_single:
                            if es.idmun.idprov.idprov == p.idprov:
                                for i in instr_single:
                                    if i.idemp_id == es.idemp and i.empiddb_id == es.empiddb and nombre == i.instnom.lower():
                                        for m in magn:
                                            if m.idmag == i.idmag_id and m.magiddb == i.magiddb_id and \
                                                    m.grpmagnom.grpmagnom == k:
                                                if valor == -1:
                                                    if exact != -1:
                                                        flag = 0
                                                        for cm in caract_met:
                                                            if exact != 1000000:
                                                                if cm.idinst_id == i.idinst and cm.instiddb_id == i.instiddb and cm.caractmeterrmax <= float(
                                                                        exact):
                                                                    flag = 1
                                                                    break
                                                            else:
                                                                if cm.idinst_id == i.idinst and cm.instiddb_id == i.instiddb and cm.caractmeterrmax >= float(
                                                                        exactitud[count_exact - 1]):
                                                                    flag = 1
                                                                    break
                                                        if flag == 1:
                                                            count_prov += check_catuso_indvisual(i, nombre)
                                                    else:
                                                        count_prov += check_catuso_indvisual(i, nombre)
                                                else:
                                                    for cm in caract_met:
                                                        if cm.idinst_id == i.idinst and cm.instiddb_id == i.instiddb:
                                                            for rng in rangos:
                                                                if cm.idrngmed_id == rng.idrngmed and \
                                                                        cm.rngmediddb_id == rng.rngmediddb:
                                                                    for r in rel:
                                                                        if rng.idrelmagunimed_id == r.idrelmagunimed and \
                                                                                rng.relmagunimediddb_id == r.relmagunimediddb:
                                                                            for um in unimed:
                                                                                if r.idunimed_id == um.idunimed and \
                                                                                        r.unimediddb_id == um.unimediddb:
                                                                                    if count == 0:
                                                                                        if float(
                                                                                                rng.rngmedlimsup) <= float(
                                                                                                valor):
                                                                                            if exact != -1:
                                                                                                if cm.caractmeterrmax == float(
                                                                                                        exact):
                                                                                                    count_prov += check_catuso_indvisual(
                                                                                                        i, nombre)
                                                                                            else:
                                                                                                count_prov += check_catuso_indvisual(
                                                                                                    i, nombre)
                                                                                    else:
                                                                                        if valor == 1000000:
                                                                                            if float(
                                                                                                    rng.rngmedlimsup) > float(
                                                                                                    lista[count - 1]):
                                                                                                count_prov += check_catuso_indvisual(
                                                                                                    i, nombre)
                                                                                        else:
                                                                                            if float(
                                                                                                    rng.rngmedliminf) > float(
                                                                                                    lista[
                                                                                                        count - 1]) and \
                                                                                                    float(
                                                                                                        rng.rngmedlimsup) <= float(
                                                                                                valor):
                                                                                                count_prov += check_catuso_indvisual(
                                                                                                    i, nombre)
                                                                                    break
                                                                    break
                                                break
                        dict_ctd_inst[p.provnom] = count_prov
                    list1 = []
                    for p in prov:
                        list1.append(dict_ctd_inst[p.provnom])
                    if valor == -1:
                        inst_per_prov.append((denom_inst, list1))
                    else:
                        if valor == 1000000:
                            if nombre == 'regla':
                                if exact == 1000000:
                                    inst_per_prov.append(('Regla mayor de ' + str(lista[count - 1]) + ' ' +
                                                          unidad_medicion + ' con valor de división mayor de ' + str(
                                        exactitud[count_exact - 1]) + ' ' + unidad_medicion, list1))
                                else:
                                    inst_per_prov.append(('Regla mayor de ' + str(lista[
                                                                                      count - 1]) + ' ' + unidad_medicion + ' con valor de división menor o igual a ' + str(
                                        exact) + ' ' + unidad_medicion,
                                                          list1))
                            else:
                                inst_per_prov.append((str(denom_inst) + ' mayor de ' + str(lista[count - 1]) + ' ' +
                                                      unidad_medicion, list1))
                        else:
                            if nombre == 'regla':
                                if exact == 1000000:
                                    inst_per_prov.append(('Regla hasta ' + str(valor) + ' ' +
                                                          unidad_medicion + ' con valor de división mayor de ' + str(
                                        exactitud[count_exact - 1]) + ' ' + unidad_medicion,
                                                          list1))
                                else:
                                    inst_per_prov.append(('Regla hasta ' + str(valor) + ' ' +
                                                          unidad_medicion + ' con valor de división menor o igual a ' + str(
                                        exact) + ' ' + unidad_medicion,
                                                          list1))
                            else:
                                inst_per_prov.append(
                                    (str(denom_inst) + ' hasta ' + str(valor) + ' ' + unidad_medicion, list1))
        inst_per_prov_per_magn.append((k, inst_per_prov))

    return inst_per_prov_per_magn


def export_informe_magnitudes():
    instrumentos_data = magnitudes_por_provincias()
    w = xlsxwriter.Workbook("static/docs/Informe Instrumentos.xlsx")
    row = 1
    column = 0
    cell_format_body = w.add_format({'font_name': 'Arial', 'font_size': 9})
    cell_format_header = w.add_format({'bold': True, 'font_name': 'Arial', 'font_size': 9, 'align': 'center'})
    for i in instrumentos_data:
        temp_sheet = w.add_worksheet(i[0])
        temp_sheet.set_column('A:A', 50)
        temp_sheet.set_column('B:SQ', 15)
        temp_sheet.write(0, 0, "Denominación", cell_format_header)
        temp_sheet.write(0, 1, "Pinar del Río", cell_format_header)
        temp_sheet.write(0, 2, "Artemisa", cell_format_header)
        temp_sheet.write(0, 3, "La Habana", cell_format_header)
        temp_sheet.write(0, 4, "Mayabeque", cell_format_header)
        temp_sheet.write(0, 5, "Matanzas", cell_format_header)
        temp_sheet.write(0, 6, "Cienfuegos", cell_format_header)
        temp_sheet.write(0, 7, "Villa Clara", cell_format_header)
        temp_sheet.write(0, 8, "Sancti Spíritus", cell_format_header)
        temp_sheet.write(0, 9, "Ciego de Ávila", cell_format_header)
        temp_sheet.write(0, 10, "Camaguey", cell_format_header)
        temp_sheet.write(0, 11, "Las Tunas", cell_format_header)
        temp_sheet.write(0, 12, "Holguín", cell_format_header)
        temp_sheet.write(0, 13, "Gramma", cell_format_header)
        temp_sheet.write(0, 14, "Santiago de Cuba", cell_format_header)
        temp_sheet.write(0, 15, "Guantánamo", cell_format_header)
        temp_sheet.write(0, 16, "Isla de la Juventud", cell_format_header)
        for k in i[1]:
            temp_sheet.write(row, column, k[0], cell_format_body)
            column += 1
            for l in k[1]:
                temp_sheet.write(row, column, l, cell_format_body)
                column += 1
            row += 1
            column = 0
        row = 1
    w.close()


def check_catuso_indvisual(inst, nombre):
    if nombre.__contains__('patrón'):
        if inst.catusonom.catusonom != 'Patrón':
            return 0
    if nombre.__contains__('analógic'):
        if inst.instindvisual == 'Analógico':
            return 1
        else:
            return 0
    else:
        if nombre.__contains__('digital'):
            if inst.instindvisual == 'Digital':
                return 1
            else:
                return 0
        else:
            return 1
        
        
def more_info(ins, inst_gen):
    empresas = Empresas.objects.all()
    for emp in empresas:
        if ins.idemp_id == emp.idemp and ins.empiddb_id == emp.empiddb:
            if emp.empnom in inst_gen:
                inst_gen[emp.empnom] += 1
            else:
                inst_gen[emp.empnom] = 1
            break
    return inst_gen
