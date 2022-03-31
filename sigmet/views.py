from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from sigmet.decorators import *
from sigmet.forms import *
from django.contrib import messages


def login_(request):
    if request.method == 'GET':
        return render(request, 'sigmet/authent/login.html')
    else:
        email = request.POST['email']
        password = request.POST['password']
        if not email or not password:
            messages.error(request, "Complete los campos")
            return render(request, 'sigmet/authent/login.html')
        else:
            input_user = MyUser.objects.get(email=email)
            if input_user is None:
                messages.error(request, "Usario no existente")
                return render(request, 'sigmet/authent/login.html')
            else:
                if not input_user.is_admin and input_user.fecha_licencia < timezone.now().date():
                    input_user.is_active = False
                    input_user.save()
                    messages.error(request, "Licencia vencida, notifique al proveedor de servicio")
                    return render(request, 'sigmet/authent/login.html')
                elif input_user.is_active:
                    user_auth = authenticate(request, username=email, password=password)
                    if user_auth is None:
                        messages.error(request, "Credenciales incorrectas")
                        return render(request, 'sigmet/authent/login.html')
                    else:
                        login(request, user_auth)
                        if "Ejecutivo" in input_user.rol:
                            return redirect('corp:index')
                        else:
                            return redirect('sigmet:index')
                else:
                    messages.error(request, "Licencia vencida, notifique al proveedor de servicio")
                    return render(request, 'sigmet/authent/login.html')


@login_required
@role_required(allowed_roles=["Administrador"])
def register_user(request):
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
            fecha_licencia = usuario_form.cleaned_data['fecha_licencia']
            admin = True
            if 'Administrador' not in rol:
                admin = False
            if pass1 and pass2 and pass1 != pass2:
                messages.error(request, "No coinciden las contraseñas")
                return render(request, 'sigmet/authent/register.html', {'form': usuario_form})
            elif fecha_licencia < timezone.now().date():
                messages.error(request, "Fecha de licencia incorrecta")
                return render(request, 'sigmet/authent/register.html', {'form': usuario_form})
            else:
                user = MyUser(email=usuario_form.cleaned_data['email'],
                              is_active=True,
                              is_admin=admin,
                              empresa=empresa,
                              fecha_licencia=fecha_licencia,
                              rol=rol,
                              password=make_password(pass1)
                              )
                try:
                    user.save()
                except (NameError, IntegrityError):
                    messages.error(request, "Usuario ya existente")
                    return render(request, 'sigmet/authent/register.html', {'form': usuario_form})
                else:
                    usuario_form = UsuarioForm()
                    messages.info(request, "Usuario creado exitosamente")
                    return render(request, 'sigmet/authent/register.html', {'form': usuario_form})
        else:
            return render(request, 'sigmet/authent/register.html', {'form': usuario_form})


@login_required
@role_required(allowed_roles=["Administrador", "Operador"])
def index(request):
    return render(request, 'sigmet/index.html')


@login_required
def logout_(request):
    logout(request)
    return redirect('sigmet:login')
