from django import forms
from sigmet.models import *


class UsuarioForm(forms.Form):
    ROL = [
        ("Administrador", "Administrador"),
        ("Ejecutivo", "Ejecutivo"),
        ("Operador", "Operador"),
    ]

    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(
                                 attrs={
                                     'class': 'form-control',
                                 }
                             )
                             )

    fecha_licencia = forms.DateField(required=True,
                                     widget=forms.DateInput(
                                         attrs={
                                             'type': 'date',
                                             'class': 'form-control',
                                         }
                                     ))

    rol = forms.ChoiceField(required=True,
                            choices=ROL,
                            widget=forms.Select(
                                attrs={
                                    'class': 'form-control',
                                }
                            ))

    empresa = forms.ModelChoiceField(
        required=True,
        queryset=EmpresaId.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                    }
                                )
                                )
