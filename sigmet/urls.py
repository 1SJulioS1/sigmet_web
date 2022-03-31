from django.urls import path
from sigmet import views

app_name = 'sigmet'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_, name='login'),
    path('lougout/', views.logout_, name='logout'),
    path('register/', views.register_user, name='register'),
]
