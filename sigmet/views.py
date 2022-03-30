from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.shortcuts import render
from sigmet.forms import *
from django.contrib import messages


def login(request):
    usuario_form = UsuarioForm()
    if request.method == 'GET':
        return render(request, 'sigmet/authent/register.html', {'form': usuario_form})
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        if usuario_form.is_valid():
            empresa = usuario_form.cleaned_data['empresa']
            empresa = EmpresaId.objects.get(nombre=empresa)
            rol = usuario_form.cleaned_data['rol'],
            pass1 = usuario_form.cleaned_data['password1']
            pass2 = usuario_form.cleaned_data['password2']
            admin = True
            if rol != 'Administrador':
                admin = False
            if pass1 and pass2 and pass1 != pass2:
                messages.error(request, "No coinciden las contraseñas")
                return render(request, 'sigmet/authent/register.html', {'form': usuario_form})
            else:
                user = MyUser(email=usuario_form.cleaned_data['email'],
                              is_active=True,
                              is_admin=admin,
                              empresa=empresa,
                              fecha_licencia=usuario_form.cleaned_data['fecha_licencia'],
                              rol=rol,
                              password=make_password(pass1)
                              )
                try:
                    user.save()
                except (NameError,IntegrityError):
                    messages.error(request, "Usuario ya existente")
                    return render(request, 'sigmet/authent/register.html', {'form': usuario_form})
                else:
                    return render(request, 'sigmet/authent/register.html', {'form': usuario_form})
        else:
            return render(request, 'sigmet/authent/register.html', {'form': usuario_form})
