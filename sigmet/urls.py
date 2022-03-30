from django.urls import path
from sigmet import views

app_name = 'sigmet'

urlpatterns = [
    path('', views.login, name='login'),
]
