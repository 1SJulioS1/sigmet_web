import json
from datetime import date

import pandas as pd
import xlsxwriter

from .models import *


def obtener_instrumentos_rango(minimo, maximo, unidad_de_medicion, instrument_subset):
    if instrument_subset == "":
        instrument_subset = Instrumentos.objects.all()
    rel = Relacionmagnitudesunidadesmedicion.objects.all()
    caract_met = Caracteristicasmetrologicas.objects.all()
    d = dict()
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
                                            d = more_info(i, d)
                                            break
    except Unidadesmedicion.DoesNotExist:
        return {0: json.dumps(dict())}

    return {count: json.dumps(d)}


def instrumentos_por_magnitud():
    grupo = Gruposmagnitudes.objects.all()
    magns = remove_duplicated_magnitudes()
    instr_single = remove_duplicated_instruments()

    inst_per_mag_per_group = dict()
    for g in grupo:
        inst_per_magns = dict()
        for m in magns:
            if m.grpmagnom == g:
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


def cantidad_inst_por_grupo(instr, magnitudes):
    elect = 0
    inst_elect = []
    d_elect = dict()
    presion = 0
    inst_presion = []
    d_presion = dict()
    temp = 0
    inst_tmp = []
    d_tmp = dict()
    flujo = 0
    d_flujo = dict()
    volumen = 0
    d_vol = dict()
    dim = 0
    d_dim = dict()
    masa = 0
    d_masa = dict()
    fuerza = 0
    d_fuerza = dict()
    fis_quim = 0
    d_fq = dict()
    dureza = 0
    d_dureza = dict()
    vibr = 0
    d_vibr = dict()
    ruido = 0
    d_ruido = dict()
    ilum = 0
    d_ilum = dict()

    for i in instr:
        for me in magnitudes:
            if i.idmag_id == me.idmag and i.magiddb_id == me.magiddb:
                if str(me.grpmagnom.grpmagnom).lower() == 'electricidad':
                    elect += 1
                    inst_elect.append(i)
                    d_elect = more_info(i, d_elect)
                else:
                    if str(me.grpmagnom.grpmagnom).lower() == 'presión':
                        presion += 1
                        inst_presion.append(i)
                        d_presion = more_info(i, d_presion)
                    else:
                        if str(me.grpmagnom.grpmagnom).lower() == 'temperatura':
                            temp += 1
                            inst_tmp.append(i)
                            d_tmp = more_info(i, d_tmp)
                        else:
                            if str(me.grpmagnom.grpmagnom).lower() == 'dimensional':
                                dim += 1
                                d_dim = more_info(i, d_dim)
                            else:
                                if str(me.grpmagnom.grpmagnom).lower() == 'dureza':
                                    dureza += 1
                                    d_dureza = more_info(i, d_dureza)
                                else:
                                    if str(me.grpmagnom.grpmagnom).lower() == 'flujo/gasto' or \
                                            str(me.grpmagnom.grpmagnom).lower() == 'flujo' or \
                                            str(me.grpmagnom.grpmagnom).lower() == 'gasto':
                                        flujo += 1
                                        d_flujo = more_info(i, d_flujo)
                                    else:
                                        if str(me.grpmagnom.grpmagnom).lower() == 'volumen' or \
                                                str(me.grpmagnom.grpmagnom).lower() == 'volúmen':
                                            volumen += 1
                                            d_vol = more_info(i, d_vol)
                                        else:
                                            if str(me.grpmagnom.grpmagnom).lower() == 'masa':
                                                masa += 1
                                                d_masa = more_info(i, d_masa)
                                            else:
                                                if str(me.grpmagnom.grpmagnom).lower().__contains__('fuerza'):
                                                    fuerza += 1
                                                    d_fuerza = more_info(i, d_fuerza)
                                                else:
                                                    if str(me.grpmagnom.grpmagnom).lower() == 'vibraciones' or \
                                                            str(me.grpmagnom.grpmagnom).lower() == 'vibración' or \
                                                            str(me.grpmagnom.grpmagnom).lower() == 'vibracion':
                                                        vibr += 1
                                                        d_vibr = more_info(i, d_vibr)
                                                    else:
                                                        if str(me.grpmagnom.grpmagnom).lower() == 'fisico-quimico' or \
                                                                str(me.grpmagnom.grpmagnom).lower() == 'físico-químico':
                                                            fis_quim += 1
                                                            d_fq = more_info(i, d_fq)
                                                        else:
                                                            if str(
                                                                    me.grpmagnom.grpmagnom).lower() == 'ruidos-sonometros' or \
                                                                    str(
                                                                        me.grpmagnom.grpmagnom).lower() == 'ruidos-sonómetros':
                                                                ruido += 1
                                                                d_ruido = more_info(i, d_ruido)
                                                            else:
                                                                if str(
                                                                        me.grpmagnom.grpmagnom).lower() == 'iluminacion-luxometros' or \
                                                                        str(
                                                                            me.grpmagnom.grpmagnom).lower() == 'iluminación-luxómetros' or \
                                                                        str(
                                                                            me.grpmagnom.grpmagnom).lower() == 'iluminacion-luxómetros' or \
                                                                        str(
                                                                            me.grpmagnom.grpmagnom).lower() == 'iluminación-luxometros':
                                                                    ilum += 1
                                                                    d_ilum = more_info(i, d_ilum)

    dictionary = {
        'elect': {elect: json.dumps(d_elect)},
        'presion': {presion: json.dumps(d_presion)},
        'temp': {temp: json.dumps(d_tmp)},
        'flujo': {flujo: json.dumps(d_flujo)},
        'volumen': {volumen: json.dumps(d_vol)},
        'dim': {dim: json.dumps(d_dim)},
        'masa': {masa: json.dumps(d_masa)},
        'fuerza': {fuerza: json.dumps(d_fuerza)},
        'fis_quim': {fis_quim: json.dumps(d_fq)},
        'dureza': {dureza: json.dumps(d_dureza)},
        'vibr': {vibr: json.dumps(d_vibr)},
        'ruido': {ruido: json.dumps(d_ruido)},
        'ilum': {ilum: json.dumps(d_ilum)},
        'inst_elect': inst_elect,
        'inst_presion': inst_presion,
        'inst_tmp': inst_tmp
    }

    return dictionary


def cantidad_patrones_por_magnitud(instr_patr, magnitudes):
    int_elec = 0
    d_elect = dict()
    ten_elec = 0
    d_ten = dict()
    res_elec = 0
    d_res = dict()

    for ip in instr_patr:
        for me in magnitudes:
            if ip.idmag_id == me.idmag and ip.magiddb_id == me.magiddb:
                if me.magnom == 'Intensidad de corriente eléctrica':
                    int_elec += 1
                    d_elect = more_info(ip, d_elect)
                    break
                else:
                    if me.magnom == 'Tensión eléctrica':
                        ten_elec += 1
                        d_ten = more_info(ip, d_ten)
                        break
                    else:
                        if me.magnom == 'Resistencia Eléctrica':
                            res_elec += 1
                            d_res = more_info(ip, d_res)
                            break
    return {int_elec: json.dumps(d_elect)}, {ten_elec: json.dumps(d_ten)}, {res_elec: json.dumps(d_res)}


def remove_duplicated_instruments():
    instrumentos = Instrumentos.objects.all()
    instr_single = []
    flag = 0
    count = 0
    for i in instrumentos:
        count += 1
        for ip in instr_single:
            if ip == i:
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
        for e1 in emp_single:
            if e1.empnom == e.empnom:
                flag = 1
                break
        if flag == 0:
            emp_single.append(e)
        flag = 0
    return emp_single


def remove_duplicated_magnitudes():
    mag = Magnitudes.objects.all()
    single_mag = []
    for m in mag:
        if m in single_mag:
            pass
        else:
            single_mag.append(m)
    return single_mag


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
                                            if cadena in miliohm:
                                                for k in miliohm[cadena]:
                                                    miliohm_dict = more_info(ins, miliohm[cadena][k])
                                                    miliohm[cadena] = {k + 1: miliohm_dict}
                                            else:
                                                miliohm_dict = more_info(ins, dict())
                                                miliohm[cadena] = {1: miliohm_dict}
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
                                                if cadena in ohm:
                                                    for k in ohm[cadena]:
                                                        ohm_dict = more_info(ins, ohm[cadena][k])
                                                        ohm[cadena] = {k + 1: ohm_dict}
                                                else:
                                                    ohm_dict = more_info(ins, dict())
                                                    ohm[cadena] = {1: ohm_dict}
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
                                                    if cadena in kiloohm:
                                                        for k in kiloohm[cadena]:
                                                            kiloohm_dict = more_info(ins, kiloohm[cadena][k])
                                                            kiloohm[cadena] = {k + 1: kiloohm_dict}
                                                    else:
                                                        kiloohm_dict = more_info(ins, dict())
                                                        kiloohm[cadena] = {1: kiloohm_dict}
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
                                                        if cadena in megaohm:
                                                            for k in megaohm[cadena]:
                                                                megaohm_dict = more_info(ins, megaohm[cadena][k])
                                                                megaohm[cadena] = {k + 1: megaohm_dict}
                                                        else:
                                                            megaohm_dict = more_info(ins, dict())
                                                            megaohm[cadena] = {1: megaohm_dict}

    for k in miliohm:
        for k1 in miliohm[k]:
            miliohm_lista.append((k, k1, json.dumps(miliohm[k][k1])))
    for k in ohm:
        for k1 in ohm[k]:
            ohm_lista.append((k, k1, json.dumps(ohm[k][k1])))
    for k in kiloohm:
        for k1 in kiloohm[k]:
            kiloohm_lista.append((k, k1, json.dumps(kiloohm[k][k1])))
    for k in megaohm:
        for k1 in megaohm[k]:
            megaohm_lista.append((k, k1, json.dumps(megaohm[k][k1])))

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
            if es.idmun.idprov == p.idprov:
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
            if es.idmun.idprov == p.idprov:
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
    emp = Empresas.objects.all()

    prov = Provincias.objects.all()
    caract_met = Caracteristicasmetrologicas.objects.all()
    rangos = Rangosmedicion.objects.all()
    magn = remove_duplicated_magnitudes()
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
                        if nombre == 'escuadra cilíndrica':
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
                                                lista = [1, 20]
                                                unidad_medicion = 'kg'
                                            else:
                                                if nombre == 'pesa clase m1-m3':
                                                    lista = [1, 5, 10, 20, 50]
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
                                                                                                                                if nombre == 'cinta de medición con plomada':
                                                                                                                                    lista = [
                                                                                                                                        30]
                                                                                                                                    unidad_medicion = 'm'
                                                                                                                                else:
                                                                                                                                    if nombre.__contains__(
                                                                                                                                            'bloque patrón grado'):
                                                                                                                                        lista = [
                                                                                                                                            100,
                                                                                                                                            500,
                                                                                                                                            1000]
                                                                                                                                        unidad_medicion = 'mm'
                                                                                                                                    else:
                                                                                                                                        if nombre == 'camión cisterna':
                                                                                                                                            lista = [
                                                                                                                                                5]
                                                                                                                                            unidad_medicion = 'm3'
                                                                                                                                        else:
                                                                                                                                            if nombre == 'medida con trazos rígida':
                                                                                                                                                lista = [
                                                                                                                                                    1,
                                                                                                                                                    1000000]
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
                                                                                                                                                else:
                                                                                                                                                    if nombre == 'termómetro líquido en vidrio':
                                                                                                                                                        lista = [
                                                                                                                                                            100,
                                                                                                                                                            300]
                                                                                                                                                        exactitud = [
                                                                                                                                                            0.1,
                                                                                                                                                            0.2,
                                                                                                                                                            0.5,
                                                                                                                                                            1]
                                                                                                                                                        unidad_medicion = '°C'
                                                                                                                                                    else:
                                                                                                                                                        if nombre == 'contador de agua doméstico':
                                                                                                                                                            lista = [
                                                                                                                                                                5]
                                                                                                                                                            unidad_medicion = 'm3/h'
                                                                                                                                                        else:
                                                                                                                                                            if nombre == 'contador de líquido de uso comercial':
                                                                                                                                                                lista = [
                                                                                                                                                                    10,
                                                                                                                                                                    60,
                                                                                                                                                                    1000000]
                                                                                                                                                                unidad_medicion = 'm3/h'

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
                        for es in emp:
                            if es.idmun.idprov == p.idprov:
                                for i in instr_single:
                                    if i.instnom == 'Equipo de rayos x':
                                        print(str(i.idemp_id) + ' ' + str(es.idemp) + ' ' + ' ' + str(
                                            i.empiddb_id) + ' ' + str(es.empiddb) + ' ' + str(nombre))
                                    if i.idemp_id == es.idemp and i.empiddb_id == es.empiddb and nombre == i.instnom.lower():  # and i.estadoinstnom == 'Uso':

                                        print(str(k))
                                        if str(k) in ['Inst. Diagnóstico', 'Estaciones Meteorológicas', 'Velocidad']:
                                            print(nombre)
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
                                        else:
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
                        # if nombre == 'equipo de rayos x':
                        #     print(p.provnom + ' : ' + str(count_prov))
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
                                if nombre == 'termómetro líquido en vidrio':
                                    if exact == 1000000:
                                        inst_per_prov.append(
                                            ('Termómetro líquido en vidrio mayor de ' + str(lista[count - 1]) + ' ' +
                                             unidad_medicion + ' con valor de división mayor de ' + str(
                                                exactitud[count_exact - 1]) + ' ' + unidad_medicion, list1))
                                    else:
                                        inst_per_prov.append(('Termómetro líquido en vidrio mayor de ' + str(lista[
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
                                if nombre == 'termómetro líquido en vidrio':
                                    if exact == 1000000:
                                        inst_per_prov.append(('Termómetro líquido en vidrio hasta ' + str(valor) + ' ' +
                                                              unidad_medicion + ' con valor de división mayor de ' + str(
                                            exactitud[count_exact - 1]) + ' ' + unidad_medicion,
                                                              list1))
                                    else:
                                        inst_per_prov.append(('Termómetro líquido en vidrio hasta ' + str(valor) + ' ' +
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
