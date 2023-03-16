# PYTHON MODULES
import inspect

# DJANGO MODULES
from django import forms
from django.conf import settings
from django.contrib.auth import _get_backends
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _


# PROJECT MODULES
from config.models import *
from offers.models import *
from offers.utils import *


class OfferForm(forms.ModelForm):
    requirements = forms.ModelMultipleChoiceField(
        queryset=Requirements.objects.all(),
        required=False,
        label="Requisitos",
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(),
        required=False,
        label="Etiquetas de búsqueda",
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields["user"].required = False
        self.fields["title"].label = "Título"
        self.fields["salary"].label = "Salario estimado"
        self.fields["currency"].label = "Moneda de pago"
        self.fields["vacancies"].label = "Vacantes"
        self.fields["modality"].label = "Modalidad"
        self.fields["city"].label = "Ciudad"
        self.fields["hiring_date"].label = "Fecha de contratación"
        self.fields["conttype"].label = "Tipo de contrato"
        self.fields["workday"].label = "Jornada"
        self.fields["payperiod"].label = "Tipo de pago"
        self.fields["description"].label = "Descripción"

    class Meta:
        model = Offers

        fields = [
            "user",
            "title",
            "salary",
            "currency",
            "vacancies",
            "modality",
            "city",
            "hiring_date",
            "conttype",
            "workday",
            "payperiod",
            "description",
            "requirements",
            "tags",
        ]

        widgets = {
            "user": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "salary": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "currency": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "vacancies": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "modality": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "city": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "hiring_date": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "conttype": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "workday": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "payperiod": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
        }
