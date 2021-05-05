from django.urls import path, include

from corp import views

app_name = 'corp'

vistas = [
    # path('', views.InstrumentoListView.as_view(), name='atriblist'),
    path('', views.cant_inst, name='index'),
]

urlpatterns = [
    path('', include(vistas))
]
