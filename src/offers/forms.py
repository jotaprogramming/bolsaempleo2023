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


class OfferAdminForm(forms.ModelForm):
    requirements = forms.ModelMultipleChoiceField(
        queryset=Requirements.objects.all(),
        required=False,
        label="Requisitos *",
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(),
        required=False,
        label="Etiquetas de búsqueda *",
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs):
        super(OfferAdminForm, self).__init__(*args, **kwargs)
        self.fields["title"].label = "Título *"
        self.fields["salary"].label = "Salario estimado *"
        self.fields["currency"].label = "Moneda de pago *"
        self.fields["vacancies"].label = "Vacantes"
        self.fields["modality"].label = "Modalidad *"
        self.fields["city"].label = "Ciudad *"
        self.fields["hiring_date"].label = "Fecha de contratación"
        self.fields["conttype"].label = "Tipo de contrato"
        self.fields["workday"].label = "Jornada"
        self.fields["payperiod"].label = "Periodo de pago"
        self.fields["hiring_date"].label = "Fecha de contratación"
        self.fields["description"].label = "Descripción *"
        self.fields["user"].required = False
        self.fields["vacancies"].required = False
        self.fields["workday"].required = False
        self.fields["conttype"].required = False
        self.fields["payperiod"].required = False

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


class OfferForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset=Countries.objects.all(),
        required=True,
        label="País *",
        widget=forms.Select(attrs={"class": "single-input"}),
    )

    district = forms.ModelChoiceField(
        queryset=Districts.objects.all(),
        required=True,
        label="Departamento *",
        widget=forms.Select(attrs={"class": "single-input"}),
    )

    city = forms.ModelChoiceField(
        queryset=Cities.objects.all(),
        required=True,
        label="Ciudad *",
        widget=forms.Select(attrs={"class": "single-input"}),
    )

    requirements = forms.ModelMultipleChoiceField(
        queryset=Requirements.objects.all(),
        required=False,
        label="Requisitos",
        widget=forms.SelectMultiple(attrs={"class": "single-input"}),
    )

    tags = forms.CharField(
        min_length=3,
        required=False,
        label="Etiquetas de búsqueda",
    )

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields["title"].label = "Título *"
        self.fields["salary"].label = "Salario estimado *"
        self.fields["currency"].label = "Moneda de pago *"
        self.fields["vacancies"].label = "Vacantes"
        self.fields["modality"].label = "Modalidad *"
        self.fields["city"].label = "Ciudad *"
        self.fields["hiring_date"].label = "Fecha de contratación"
        self.fields["conttype"].label = "Tipo de contrato"
        self.fields["workday"].label = "Jornada"
        self.fields["payperiod"].label = "Periodo de pago"
        self.fields["hiring_date"].label = "Fecha de contratación"
        self.fields["description"].label = "Descripción *"
        self.fields["user"].required = False
        self.fields["vacancies"].required = False
        self.fields["workday"].required = False
        self.fields["conttype"].required = False
        self.fields["payperiod"].required = False

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
        ]

        widgets = {
            "user": forms.Select(
                attrs={
                    "class": "single-input",
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "single-input",
                }
            ),
            "salary": forms.NumberInput(
                attrs={
                    "class": "single-input",
                }
            ),
            "currency": forms.Select(
                attrs={
                    "class": "single-input",
                }
            ),
            "vacancies": forms.NumberInput(
                attrs={
                    "class": "single-input",
                }
            ),
            "modality": forms.Select(
                attrs={
                    "class": "single-input",
                }
            ),
            "city": forms.Select(
                attrs={
                    "class": "single-input",
                }
            ),
            "hiring_date": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "single-input", "type": "date"}
            ),
            "conttype": forms.Select(
                attrs={
                    "class": "single-input",
                }
            ),
            "workday": forms.Select(
                attrs={
                    "class": "single-input",
                }
            ),
            "payperiod": forms.Select(
                attrs={
                    "class": "single-input",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "single-input",
                }
            ),
        }


class CandidatureStatusEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CandidatureStatusEditForm, self).__init__(*args, **kwargs)
        self.fields["status"].label = "Estado"
        self.fields["status"].required = False

    class Meta:
        model = Candidatures

        fields = [
            "status",
        ]


class CandidatureUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CandidatureUpdateForm, self).__init__(*args, **kwargs)
        self.fields["status"].label = "Estado"
        self.fields["status"].required = False

    class Meta:
        model = Candidatures

        fields = [
            "status",
        ]

        widgets = {
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }
