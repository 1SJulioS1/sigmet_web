# from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'corp'

urlpatterns = [
    # path('', views.prueba2),
    path('', views.principal, name='principal'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', login_required(views.cant_inst, redirect_field_name=''), name='index'),
    path('gener/', login_required(views.generalidades_instrumento, redirect_field_name=''),
         name='generalidades_instrumento'),
    path('gener/instr-ind_visual/data/', login_required(views.instrumentos_indicacion_data, redirect_field_name=''),
         name='instrumento_ind_visual_data'),
    path('magn/', login_required(views.magnitud_instrumento, redirect_field_name=''), name='magnitud_instrumento'),
    path('rango/gen/', login_required(views.instrumentos_trabajo_gen, redirect_field_name=''),
         name='instrumento_trabajo_gen'),
    path('rango/pc/', login_required(views.instrumentos_trabajo_pc, redirect_field_name=''),
         name='instrumento_trabajo_pc'),
    path('rango/explot/', login_required(views.instrumentos_trabajo_explot, redirect_field_name=''),
         name='instrumento_trabajo_explot'),
    path('rango/fab/', login_required(views.instrumentos_trabajo_fabr, redirect_field_name=''),
         name='instrumento_trabajo_fab'),
    path('patron/', login_required(views.patrones, redirect_field_name=''), name='patron_instrumento'),
    path('magn/export/', login_required(views.informe_magnitudes, redirect_field_name=''), name='export_mag')
]
