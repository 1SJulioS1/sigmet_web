# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Ajustes(models.Model):
    idemp = models.ForeignKey('Empresas', models.DO_NOTHING, db_column='IdEmp',
                              primary_key=True, related_name='idemploc_Empresa')  # Field name made lowercase.
    desde = models.DateField(db_column='Desde', blank=True, null=True)  # Field name made lowercase.
    hasta = models.DateField(db_column='Hasta', blank=True, null=True)  # Field name made lowercase.
    empiddb = models.ForeignKey('Empresas', models.DO_NOTHING, db_column='EmpIdDB',
                                related_name='empiddbajuste_empresa')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ajustes'
        unique_together = (('idemp', 'empiddb'),)


class Atributosprocesoscorporativos(models.Model):
    atribproccorpnom = models.CharField(db_column='AtribProcCorpNom', primary_key=True,
                                        max_length=50)  # Field name made lowercase.
    atribproccorpiddb = models.IntegerField(db_column='AtribProcCorpIdDB')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AtributosProcesosCorporativos'
        unique_together = (('atribproccorpnom', 'atribproccorpiddb'),)


class Caracteristicasmetrologicas(models.Model):
    idcaractmet = models.AutoField(db_column='IdCaractMet', primary_key=True)  # Field name made lowercase.
    idinst = models.ForeignKey('Instrumentos', models.DO_NOTHING, db_column='IdInst',
                               related_name='idinstcaract_instrumento')  # Field name made lowercase.
    idrngmed = models.ForeignKey('Rangosmedicion', models.DO_NOTHING,
                                 db_column='IdRngMed')  # Field name made lowercase.
    idsenhalunif = models.ForeignKey('Sealesunificadas', models.DO_NOTHING, db_column='IdSeñalUnif', blank=True,
                                     null=True,
                                     related_name='idsenhalunif_senhal_unificada')  # Field name made lowercase.
    caractmeterrmax = models.FloatField(db_column='CaractMetErrMax', blank=True,
                                        null=True)  # Field name made lowercase.
    caractmetres = models.FloatField(db_column='CaractMetRes', blank=True, null=True)  # Field name made lowercase.
    caractmetesperrmax = models.IntegerField(db_column='CaractMetEspErrMax', blank=True,
                                             null=True)  # Field name made lowercase.
    caractmetindvis = models.BooleanField(db_column='CaractMetIndVis', blank=True,
                                          null=True)  # Field name made lowercase.
    caractmettipoindvis = models.CharField(db_column='CaractMetTipoIndVis', max_length=50, blank=True,
                                           null=True)  # Field name made lowercase.
    caractmetcantdivi = models.IntegerField(db_column='CaractMetCantDivi', blank=True,
                                            null=True)  # Field name made lowercase.
    caractmetriddb = models.IntegerField(db_column='CaractMetrIdDB')  # Field name made lowercase.
    instiddb = models.ForeignKey('Instrumentos', models.DO_NOTHING, db_column='InstIdDB',
                                 related_name='instiddbcaract_instrumento')  # Field name made lowercase.
    rngmediddb = models.ForeignKey('Rangosmedicion', models.DO_NOTHING,
                                   db_column='RngMedIdDB',
                                   related_name='rngmediddb_rango_medicion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CaracteristicasMetrologicas'
        unique_together = (('idcaractmet', 'caractmetriddb'),)


class Cargos(models.Model):
    cargonom = models.CharField(db_column='CargoNom', primary_key=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cargos'


class Categoriasinstrumentos(models.Model):
    catinstnom = models.CharField(db_column='CatInstNom', primary_key=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CategoriasInstrumentos'


class Categoriasusos(models.Model):
    catusonom = models.CharField(db_column='CatUsoNom', primary_key=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CategoriasUsos'


class Centrocosto(models.Model):
    centrocostonom = models.CharField(db_column='CentroCostoNom', primary_key=True,
                                      max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CentroCosto'


class Certificados(models.Model):
    idcert = models.AutoField(db_column='IdCert', primary_key=True)  # Field name made lowercase.
    idinst = models.ForeignKey('Instrumentos', models.DO_NOTHING, db_column='IdInst',
                               related_name='idinstcert_instrumento')  # Field name made lowercase.
    certno = models.CharField(db_column='CertNo', max_length=50)  # Field name made lowercase.
    certtipo = models.CharField(db_column='CertTipo', max_length=50)  # Field name made lowercase.
    idmetodo = models.ForeignKey('Metodoscalibracionverificacion', models.DO_NOTHING, db_column='IdMetodo', blank=True,
                                 null=True, related_name='idmetodo_meotodo')  # Field name made lowercase.
    idempserv = models.ForeignKey('Empresasserviciadoras', models.DO_NOTHING, db_column='IdEmpServ', blank=True,
                                  null=True,
                                  related_name='idempservcert_empresa_serviciadora')  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase.
    resultado = models.CharField(db_column='Resultado', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    certfecha = models.DateField(db_column='CertFecha', blank=True, null=True)  # Field name made lowercase.
    empserviddb = models.ForeignKey('Empresasserviciadoras', models.DO_NOTHING,
                                    db_column='EmpServIdDB',
                                    related_name='empserviddbcert_empresa_serviciadora')  # Field name made lowercase.
    instiddb = models.ForeignKey('Instrumentos', models.DO_NOTHING, db_column='InstIdDB',
                                 related_name='instiddbcert_instrumento')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Certificados'


class Cindicionesambientalesinstrumentos(models.Model):
    idcondamb = models.ForeignKey('Condicionesambientales', models.DO_NOTHING, db_column='IdCondAmb',
                                  primary_key=True,
                                  related_name='idcondamb_condicion_ambiental')  # Field name made lowercase.
    idinst = models.ForeignKey('Instrumentos', models.DO_NOTHING, db_column='IdInst',
                               related_name='idinstcind_instrumento')  # Field name made lowercase.
    condambinstval = models.FloatField(db_column='CondAmbInstVal', blank=True, null=True)  # Field name made lowercase.
    instiddb = models.ForeignKey('Instrumentos', models.DO_NOTHING, db_column='InstIdDB',
                                 related_name='instdb_instrumento')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CindicionesAmbientalesInstrumentos'
        unique_together = (('idcondamb', 'idinst'),)


class Condicionesambientales(models.Model):
    idcondamb = models.AutoField(db_column='IdCondAmb', primary_key=True)  # Field name made lowercase.
    condambnom = models.CharField(db_column='CondAmbNom', max_length=50)  # Field name made lowercase.
    idrelmagunimed = models.ForeignKey('Relacionmagnitudesunidadesmedicion', models.DO_NOTHING,
                                       db_column='IdRelMagUniMed', blank=True, null=True,
                                       related_name='idtelmagunimed_idrelmagunimed')  # Field name made lowercase.
    tipocondambnom = models.ForeignKey('Tipocondicionesambientales', models.DO_NOTHING,
                                       db_column='TipoCondAmbNom',
                                       related_name='tipocondamb_tipo_cond_amb')  # Field name made lowercase.
    relmagunimediddb = models.ForeignKey('Relacionmagnitudesunidadesmedicion', models.DO_NOTHING,
                                         db_column='RelMagUniMedIdDB',
                                         related_name='relmagunimediddb_relacion_magnitud_unimeddb')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CondicionesAmbientales'


class Controlmetrologicosistemascadenasmedida(models.Model):
    idcontmetsistcadmed = models.AutoField(db_column='IdContMetSistCadMed',
                                           primary_key=True)  # Field name made lowercase.
    idsistcadmed = models.ForeignKey('Sistemascadenasdemedida', models.DO_NOTHING, db_column='IdSistCadMed', blank=True,
                                     null=True,
                                     related_name='idsistcadmed_sistema_cadena_med')  # Field name made lowercase.
    contmetfechaplan = models.DateField(db_column='ContMetFechaPlan', blank=True,
                                        null=True)  # Field name made lowercase.
    contmetfechaejec = models.DateField(db_column='ContMetFechaEjec', blank=True,
                                        null=True)  # Field name made lowercase.
    idprovserv = models.ForeignKey('Empresasserviciadoras', models.DO_NOTHING, db_column='IdProvServ', blank=True,
                                   null=True,
                                   related_name='idprovserv_empresa_serviciadora')  # Field name made lowercase.
    contmetresultado = models.CharField(db_column='ContMetResultado', max_length=50, blank=True,
                                        null=True)  # Field name made lowercase.
    contmetobservaciones = models.TextField(db_column='ContMetObservaciones', blank=True,
                                            null=True)  # Field name made lowercase.
    empserviddb = models.ForeignKey('Empresasserviciadoras', models.DO_NOTHING,
                                    db_column='EmpServIdDB',
                                    related_name='empserviddb_empresa_serv')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ControlMetrologicoSistemasCadenasMedida'


class Empresas(models.Model):
    idemp = models.AutoField(db_column='IdEmp', primary_key=True)  # Field name made lowercase.
    empcod = models.CharField(db_column='EmpCod', max_length=50, blank=True, null=True)  # Field name made lowercase.
    empnom = models.TextField(db_column='EmpNom', blank=True, null=True)  # Field name made lowercase.
    empnomcom = models.CharField(db_column='EmpNomCom', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    empdir = models.CharField(db_column='EmpDir', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idmun = models.ForeignKey('Municipios', models.DO_NOTHING, db_column='IdMun', blank=True,
                              null=True, related_name='idmun_municipio')  # Field name made lowercase.
    emprepres = models.CharField(db_column='EmpRepres', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    emptelef = models.CharField(db_column='EmpTelef', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    empfax = models.CharField(db_column='EmpFax', max_length=50, blank=True, null=True)  # Field name made lowercase.
    empemail = models.CharField(db_column='EmpEmail', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    empweb = models.CharField(db_column='EmpWeb', max_length=50, blank=True, null=True)  # Field name made lowercase.
    empparent = models.ForeignKey('self', models.DO_NOTHING, db_column='EmpParent', blank=True,
                                  null=True, related_name='empparent_empresa')  # Field name made lowercase.
    empiddb = models.IntegerField(db_column='EmpIdDB')  # Field name made lowercase.
    empparent_empiddb = models.ForeignKey('self', models.DO_NOTHING,
                                          db_column='EmpParent_EmpIdDB',
                                          related_name='emprparent_empiddb_empresa')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Empresas'
        unique_together = (('idemp', 'empiddb'),)


class Empresasserviciadoras(models.Model):
    idempserv = models.AutoField(db_column='IdEmpServ', primary_key=True)  # Field name made lowercase.
    empservnom = models.CharField(db_column='EmpServNom', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    empservnomcom = models.CharField(db_column='EmpServNomCom', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    empserviddb = models.IntegerField(db_column='EmpServIdDB')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EmpresasServiciadoras'
        unique_together = (('idempserv', 'empserviddb'),)


class Estadosinstrumentos(models.Model):
    estadoinstnom = models.CharField(db_column='EstadoInstNom', primary_key=True,
                                     max_length=50)  # Field name made lowercase.
    estadoinstiddb = models.IntegerField(db_column='EstadoInstIdDB')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EstadosInstrumentos'
        unique_together = (('estadoinstnom', 'estadoinstiddb'),)


class Gruposmagnitudes(models.Model):
    grpmagnom = models.CharField(db_column='GrpMagNom', primary_key=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GruposMagnitudes'


class Instrumentos(models.Model):
    idinst = models.AutoField(db_column='IdInst', primary_key=True)  # Field name made lowercase.
    idemp = models.ForeignKey('Localizaciones', models.DO_NOTHING, db_column='IdEmp', blank=True, null=True,
                              related_name='idemp_localizacion')  # Field name made lowercase.
    locnom = models.ForeignKey('Localizaciones', models.DO_NOTHING, db_column='LocNom', blank=True,
                               null=True, related_name='locnom_localizacion')  # Field name made lowercase.
    instnom = models.CharField(db_column='InstNom', max_length=50, blank=True, null=True)  # Field name made lowercase.
    instdescripcion = models.TextField(db_column='InstDescripcion', blank=True, null=True)  # Field name made lowercase.
    instmarca = models.CharField(db_column='InstMarca', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    instmodelo = models.CharField(db_column='InstModelo', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    instnoserie = models.CharField(db_column='InstNoSerie', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    instnoinv = models.CharField(db_column='InstNoInv', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    instanhofab = models.CharField(db_column='InstAñoFab', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    instpais = models.CharField(db_column='InstPais', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    idmag = models.ForeignKey('Magnitudes', models.DO_NOTHING, db_column='IdMag', blank=True,
                              null=True, related_name='idmag_magnitud')  # Field name made lowercase.
    catusonom = models.ForeignKey(Categoriasusos, models.DO_NOTHING, db_column='CatUsoNom', blank=True,
                                  null=True, related_name='catusonom_categoria_uso')  # Field name made lowercase.
    catinstnom = models.ForeignKey(Categoriasinstrumentos, models.DO_NOTHING, db_column='CatInstNom', blank=True,
                                   null=True,
                                   related_name='catinstnom_categoria_instrumento')  # Field name made lowercase.
    instindvisual = models.CharField(db_column='InstIndVisual', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    estadoinstnom = models.ForeignKey(Estadosinstrumentos, models.DO_NOTHING, db_column='EstadoInstNom', blank=True,
                                      null=True,
                                      related_name='estadoinstnom_estodo_instrumento')  # Field name made lowercase.
    idrelatribproccorp = models.ForeignKey('Relacionatributosprocesos', models.DO_NOTHING,
                                           db_column='IdRelAtribProcCorp', blank=True,
                                           null=True,
                                           related_name='idrelatribproccorp_relacion_atributo_proceso')  # Field name made lowercase.
    instfechapuestoserv = models.DateField(db_column='InstFechaPuestoServ', blank=True,
                                           null=True)  # Field name made lowercase.
    instreqcal = models.BooleanField(db_column='InstReqCal', blank=True, null=True)  # Field name made lowercase.
    instperiodocal = models.IntegerField(db_column='InstPeriodoCal', blank=True,
                                         null=True)  # Field name made lowercase.
    instfechacal = models.DateField(db_column='InstFechaCal', blank=True, null=True)  # Field name made lowercase.
    instreqver = models.BooleanField(db_column='InstReqVer', blank=True, null=True)  # Field name made lowercase.
    instperiodover = models.IntegerField(db_column='InstPeriodoVer', blank=True,
                                         null=True)  # Field name made lowercase.
    instfechaver = models.DateField(db_column='InstFechaVer', blank=True, null=True)  # Field name made lowercase.
    instespanel = models.BooleanField(db_column='InstEsPanel', blank=True, null=True)  # Field name made lowercase.
    instancho = models.FloatField(db_column='InstAncho', blank=True, null=True)  # Field name made lowercase.
    instlargo = models.FloatField(db_column='InstLargo', blank=True, null=True)  # Field name made lowercase.
    instalto = models.FloatField(db_column='InstAlto', blank=True, null=True)  # Field name made lowercase.
    instescircular = models.BooleanField(db_column='InstEsCircular', blank=True,
                                         null=True)  # Field name made lowercase.
    instradio = models.FloatField(db_column='InstRadio', blank=True, null=True)  # Field name made lowercase.
    instreqcompint = models.BooleanField(db_column='InstReqCompInt', blank=True,
                                         null=True)  # Field name made lowercase.
    estadoinstiddb = models.ForeignKey(Estadosinstrumentos, models.DO_NOTHING,
                                       db_column='EstadoInstIdDB',
                                       related_name='estadoinstiddb_estado_instrumento')  # Field name made lowercase.
    empiddb = models.ForeignKey(Empresas, models.DO_NOTHING, db_column='EmpIdDB',
                                related_name='empiddb_empresas')  # Field name made lowercase.
    instiddb = models.IntegerField(db_column='InstIdDB')  # Field name made lowercase.
    loc_empiddb = models.ForeignKey('Localizaciones', models.DO_NOTHING,
                                    db_column='Loc_EmpIdDB',
                                    related_name='loc_empiddb_localizacion')  # Field name made lowercase.
    lociddb = models.ForeignKey('Localizaciones', models.DO_NOTHING, db_column='LocIdDB',
                                related_name='lociddb_localizacion')  # Field name made lowercase.
    relatribprociddb = models.ForeignKey('Relacionatributosprocesos', models.DO_NOTHING,
                                         db_column='RelAtribProcIdDB',
                                         related_name='relatribprociddb_relacion_atributo_proceso')  # Field name made lowercase.
    magiddb = models.ForeignKey('Magnitudes', models.DO_NOTHING, db_column='MagIdDB',
                                related_name='magiddb_magnitud')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Instrumentos'
        unique_together = (('idinst', 'instiddb'),)


class Localizaciones(models.Model):
    idemp = models.ForeignKey(Empresas, models.DO_NOTHING, db_column='IdEmp',
                              primary_key=True, related_name='idemp_empresa')  # Field name made lowercase.
    locnom = models.CharField(db_column='LocNom', max_length=50)  # Field name made lowercase.
    empiddb = models.ForeignKey(Empresas, models.DO_NOTHING, db_column='EmpIdDB',
                                related_name='empiddb_empresa')  # Field name made lowercase.
    lociddb = models.IntegerField(db_column='LocIdDB')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Localizaciones'
        unique_together = (('idemp', 'locnom', 'empiddb', 'lociddb'),)


class Lugares(models.Model):
    lugarmov = models.CharField(db_column='LugarMov', primary_key=True, max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Lugares'


class Magnitudes(models.Model):
    idmag = models.AutoField(db_column='IdMag', primary_key=True)  # Field name made lowercase.
    grpmagnom = models.ForeignKey(Gruposmagnitudes, models.DO_NOTHING,
                                  db_column='GrpMagNom')  # Field name made lowercase.
    magnom = models.CharField(db_column='MagNom', max_length=50)  # Field name made lowercase.
    magiddb = models.IntegerField(db_column='MagIdDB')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Magnitudes'
        unique_together = (('idmag', 'magiddb'),)


class Metodoscalibracionverificacion(models.Model):
    idmetodo = models.AutoField(db_column='IdMetodo', primary_key=True)  # Field name made lowercase.
    metodonombre = models.CharField(db_column='MetodoNombre', max_length=50)  # Field name made lowercase.
    metodonorm = models.CharField(db_column='MetodoNorm', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MetodosCalibracionVerificacion'


class Movimientos(models.Model):
    idinst = models.ForeignKey(Instrumentos, models.DO_NOTHING, db_column='IdInst',
                               primary_key=True, related_name='idinstmov_instrumento')  # Field name made lowercase.
    tipomov = models.CharField(db_column='TipoMov', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lugarmov = models.ForeignKey(Lugares, models.DO_NOTHING, db_column='LugarMov', blank=True,
                                 null=True, related_name='lugarmov_lugar')  # Field name made lowercase.
    comentario = models.TextField(db_column='Comentario', blank=True, null=True)  # Field name made lowercase.
    instiddb = models.ForeignKey(Instrumentos, models.DO_NOTHING, db_column='InstIdDB',
                                 related_name='instddb_instrumento')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Movimientos'
        unique_together = (('idinst', 'instiddb'),)


class Municipios(models.Model):
    idmun = models.AutoField(db_column='IdMun', primary_key=True)  # Field name made lowercase.
    idprov = models.ForeignKey('Provincias', models.DO_NOTHING, db_column='IdProv', blank=True,
                               null=True)  # Field name made lowercase.
    munnom = models.CharField(db_column='MunNom', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Municipios'


class Permisos(models.Model):
    idemp = models.IntegerField(db_column='IdEmp', blank=True, null=True)  # Field name made lowercase.
    usernom = models.CharField(db_column='UserNom', max_length=50, blank=True, null=True)  # Field name made lowercase.
    userperm = models.CharField(db_column='UserPerm', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Permisos'


class Planmantenimiento(models.Model):
    idplan = models.IntegerField(db_column='IdPlan', primary_key=True)  # Field name made lowercase.
    fechaplan = models.DateField(db_column='FechaPlan', blank=True, null=True)  # Field name made lowercase.
    fechaejec = models.DateField(db_column='FechaEjec', blank=True, null=True)  # Field name made lowercase.
    idempserv = models.ForeignKey(Empresasserviciadoras, models.DO_NOTHING, db_column='IdEmpServ', blank=True,
                                  null=True,
                                  related_name='idempserv_empresa_serviciadora')  # Field name made lowercase.
    idinst = models.ForeignKey(Instrumentos, models.DO_NOTHING, db_column='IdInst', blank=True,
                               null=True, related_name='idinstplanmant_instrumento')  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase.
    instiddb = models.ForeignKey(Instrumentos, models.DO_NOTHING, db_column='InstIdDB',
                                 related_name='instiddb_instrumento')  # Field name made lowercase.
    planmttoiddb = models.IntegerField(db_column='PlanMttoIdDB')  # Field name made lowercase.
    empserviddb = models.ForeignKey(Empresasserviciadoras, models.DO_NOTHING,
                                    db_column='EmpServIdDB',
                                    related_name='empserviddb_plan_mant')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PlanMantenimiento'
        unique_together = (('idplan', 'planmttoiddb'),)


class Planes(models.Model):
    idplan = models.AutoField(db_column='IdPlan', primary_key=True)  # Field name made lowercase.
    idinst = models.ForeignKey(Instrumentos, models.DO_NOTHING, db_column='IdInst', blank=True,
                               null=True, related_name='idinstplan_instrumento')  # Field name made lowercase.
    fechaplan = models.DateField(db_column='FechaPlan', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idcert = models.ForeignKey(Certificados, models.DO_NOTHING, db_column='IdCert', blank=True,
                               null=True, related_name='idcert_certificado')  # Field name made lowercase.
    instiddb = models.ForeignKey(Instrumentos, models.DO_NOTHING, db_column='InstIdDB',
                                 related_name='insiddb_instrumento')  # Field name made lowercase.
    planesiddb = models.IntegerField(db_column='PlanesIdDB')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Planes'
        unique_together = (('idplan', 'planesiddb'),)


class Procesoscorporativos(models.Model):
    proccorpnom = models.CharField(db_column='ProcCorpNom', primary_key=True,
                                   max_length=50)  # Field name made lowercase.
    proccorpiddb = models.IntegerField(db_column='ProcCorpIdDB')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ProcesosCorporativos'
        unique_together = (('proccorpnom', 'proccorpiddb'),)


class Provincias(models.Model):
    idprov = models.AutoField(db_column='IdProv', primary_key=True)  # Field name made lowercase.
    provnom = models.CharField(db_column='ProvNom', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Provincias'


class Rangosmedicion(models.Model):
    idrngmed = models.AutoField(db_column='IdRngMed', primary_key=True)  # Field name made lowercase.
    rngmedlimsup = models.CharField(db_column='RngMedLimSup', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    rngmedliminf = models.CharField(db_column='RngMedLimInf', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    idrelmagunimed = models.ForeignKey('Relacionmagnitudesunidadesmedicion', models.DO_NOTHING,
                                       db_column='IdRelMagUniMed',
                                       related_name='idrelmagunimed_relacion_mag_unimed')  # Field name made lowercase.
    rngmediddb = models.IntegerField(db_column='RngMedIdDB')  # Field name made lowercase.
    relmagunimediddb = models.ForeignKey('Relacionmagnitudesunidadesmedicion', models.DO_NOTHING,
                                         db_column='RelMagUniMedIdDB',
                                         related_name='relmagunimediddb_relacion_mag_unid_med')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RangosMedicion'
        unique_together = (('idrngmed', 'rngmediddb'),)


class Relacionatributosprocesos(models.Model):
    idrelatribproccorp = models.AutoField(db_column='IdRelAtribProcCorp',
                                          primary_key=True)  # Field name made lowercase.
    proccorpnom = models.ForeignKey(Procesoscorporativos, models.DO_NOTHING, db_column='ProcCorpNom', blank=True,
                                    null=True, related_name='proccorpnom_proceso_corp')  # Field name made lowercase.
    atribproccorpnom = models.ForeignKey(Atributosprocesoscorporativos, models.DO_NOTHING, db_column='AtribProcCorpNom',
                                         blank=True, null=True,
                                         related_name='atribproccorpnom_atrib_proc_corp')  # Field name made lowercase.
    proccorpiddb = models.ForeignKey(Procesoscorporativos, models.DO_NOTHING,
                                     db_column='ProcCorpIdDB',
                                     related_name='proccorpiddb_proc_corp')  # Field name made lowercase.
    atribproccorpiddb = models.ForeignKey(Atributosprocesoscorporativos, models.DO_NOTHING,
                                          db_column='AtribProcCorpIdDB',
                                          related_name='atribproccorpiddb_atrib_proc_corp')  # Field name made lowercase.
    relatribprociddb = models.IntegerField(db_column='RelAtribProcIdDB')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RelacionAtributosProcesos'
        unique_together = (('idrelatribproccorp', 'relatribprociddb'),)


class Relacionmagnitudesunidadesmedicion(models.Model):
    idrelmagunimed = models.AutoField(db_column='IdRelMagUniMed', primary_key=True)  # Field name made lowercase.
    idmag = models.ForeignKey(Magnitudes, models.DO_NOTHING, db_column='IdMag',
                              related_name='idmag_mag')  # Field name made lowercase.
    idunimed = models.ForeignKey('Unidadesmedicion', models.DO_NOTHING,
                                 db_column='IdUniMed', related_name='idunimed_unid_med')  # Field name made lowercase.
    magiddb = models.ForeignKey(Magnitudes, models.DO_NOTHING, db_column='MagIdDB',
                                related_name='madiddb_mag')  # Field name made lowercase.
    unimediddb = models.ForeignKey('Unidadesmedicion', models.DO_NOTHING,
                                   db_column='UniMedIdDB',
                                   related_name='unidmediddb_unid_med')  # Field name made lowercase.
    relmagunimediddb = models.IntegerField(db_column='RelMagUniMedIdDB')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RelacionMagnitudesUnidadesMedicion'
        unique_together = (('idrelmagunimed', 'relmagunimediddb'),)


class Sealesunificadas(models.Model):
    idsenhalunif = models.IntegerField(db_column='IdSeñalUnif', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SeñalesUnificadas'


class Sistemascadenasdemedida(models.Model):
    idsistcadmed = models.AutoField(db_column='IdSistCadMed', primary_key=True)  # Field name made lowercase.
    sistcadmedtipo = models.CharField(db_column='SistCadMedTipo', max_length=50, blank=True,
                                      null=True)  # Field name made lowercase.
    sistcadmednom = models.TextField(db_column='SistCadMedNom', blank=True, null=True)  # Field name made lowercase.
    idemp = models.ForeignKey(Empresas, models.DO_NOTHING, db_column='IdEmp', blank=True,
                              null=True, related_name='idempsist_empresa')  # Field name made lowercase.
    idrngmed = models.ForeignKey(Rangosmedicion, models.DO_NOTHING, db_column='IdRngMed', blank=True,
                                 null=True, related_name='idrngmed_rango_med')  # Field name made lowercase.
    sistcadmedperiodocal = models.IntegerField(db_column='SistCadMedPeriodoCal', blank=True,
                                               null=True)  # Field name made lowercase.
    sistcadmedfechacal = models.DateField(db_column='SistCadMedFechaCal', blank=True,
                                          null=True)  # Field name made lowercase.
    empiddb = models.ForeignKey(Empresas, models.DO_NOTHING, db_column='EmpIdDB',
                                related_name='empiddbsistcad_emp')  # Field name made lowercase.
    rngmediddb = models.ForeignKey(Rangosmedicion, models.DO_NOTHING,
                                   db_column='RngMedIdDB',
                                   related_name='rngmediddb_rang_med')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SistemasCadenasDeMedida'


class Tipocondicionesambientales(models.Model):
    tipocondambnom = models.CharField(db_column='TipoCondAmbNom', primary_key=True,
                                      max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipoCondicionesAmbientales'


class Unidadesmedicion(models.Model):
    idunimed = models.AutoField(db_column='IdUniMed', primary_key=True)  # Field name made lowercase.
    unimedsim = models.CharField(db_column='UniMedSim', max_length=50)  # Field name made lowercase.
    unimednom = models.CharField(db_column='UniMedNom', max_length=50)  # Field name made lowercase.
    unimedsi = models.BooleanField(db_column='UniMedSI')  # Field name made lowercase.
    unimediddb = models.IntegerField(db_column='UniMedIdDB')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UnidadesMedicion'
        unique_together = (('idunimed', 'unimediddb'),)


class Usuarios(models.Model):
    idusuario = models.AutoField(db_column='IdUsuario', primary_key=True)  # Field name made lowercase.
    usuarionom = models.CharField(db_column='UsuarioNom', max_length=50)  # Field name made lowercase.
    usuariopassw = models.CharField(db_column='UsuarioPassw', max_length=50)  # Field name made lowercase.
    idemp = models.ForeignKey(Empresas, models.DO_NOTHING, db_column='IdEmp', blank=True,
                              null=True, related_name='idempusuarios_emp')  # Field name made lowercase.
    usuariotipo = models.CharField(db_column='UsuarioTipo', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    empiddb = models.ForeignKey(Empresas, models.DO_NOTHING, db_column='EmpIdDB',
                                related_name='empiddbusuario_emp')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Usuarios'
        unique_together = (('idemp', 'usuarionom'),)
