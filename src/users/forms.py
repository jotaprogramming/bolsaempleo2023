# DJANGO MODULES
from django import forms
from django.conf import settings

# PROJECT MODULES
from users.models import *


class UserGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserGroupForm, self).__init__(*args, **kwargs)
        self.fields["group_name"].label = "Nombre"
        self.fields["description"].label = "Descripción"

    class Meta:
        model = UserGroups

        fields = [
            "group_name",
            "description",
        ]

        widgets = {
            "group_name": forms.TextInput(
                attrs={
                    "placeholder": "Nombre del grupo",
                    "class": "form-control",
                    "minlength": "1",
                    "maxlength": "50",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Descripción del grupo",
                    "class": "form-control",
                }
            ),
        }

    def clean(self):
        datos = self.cleaned_data


class FormDelete(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormDelete, self).__init__(*args, **kwargs)
        self.fields["deleted_at"].required = False

    class Meta:
        model = UserGroups

        fields = [
            "deleted_at",
        ]

        widgets = {
            "deleted_at": forms.TextInput(
                attrs={
                    "placeholder": "Nombre del grupo",
                    "class": "form-control",
                    "minlength": "1",
                    "maxlength": "50",
                }
            ),
        }


class RestrictionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RestrictionForm, self).__init__(*args, **kwargs)
        self.fields["code"].label = "Código"
        self.fields["name"].label = "Nombre"
        self.fields["description"].label = "Descripción"

    class Meta:
        model = Restrictions

        fields = [
            "code",
            "name",
            "description",
        ]

        widgets = {
            "code": forms.TextInput(
                attrs={
                    "placeholder": "Código de la restricción",
                    "class": "form-control",
                    "minlength": "1",
                    "maxlength": "3",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Nombre de la restricción",
                    "class": "form-control",
                    "minlength": "1",
                    "maxlength": "25",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Descripción de la restricción",
                    "class": "form-control",
                }
            ),
        }

    def clean(self):
        datos = self.cleaned_data


class AppForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AppForm, self).__init__(*args, **kwargs)
        self.fields["description"].label = "Descripción"

    class Meta:
        model = Apps

        fields = [
            "description",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Descripción de la aplicación",
                    "class": "form-control",
                }
            ),
        }

    def clean(self):
        datos = self.cleaned_data


class RoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.fields["role_name"].label = "Nombre"
        self.fields["description"].label = "Descripción"

    class Meta:
        model = Roles

        fields = [
            "role_name",
            "description",
        ]

        widgets = {
            "role_name": forms.TextInput(
                attrs={
                    "placeholder": "Nombre del rol",
                    "class": "form-control",
                    "minlength": "1",
                    "maxlength": "50",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Descripción del rol",
                    "class": "form-control",
                }
            ),
        }

    def clean(self):
        datos = self.cleaned_data


class RuleForm(forms.ModelForm):
    app = forms.ModelMultipleChoiceField(
        queryset=Apps.objects.filter(deleted_at=None),
        required=True,
        label="Aplicación",
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )

    role = forms.ModelMultipleChoiceField(
        queryset=Roles.objects.filter(deleted_at=None),
        required=True,
        label="Rol",
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )

    restriction = forms.ModelMultipleChoiceField(
        queryset=Restrictions.objects.filter(deleted_at=None),
        required=False,
        label="Restricción",
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs):
        super(RuleForm, self).__init__(*args, **kwargs)
        self.fields["code"].label = "Código"
        self.fields["app"].label = "Aplicación"

    class Meta:
        model = Rules

        fields = [
            "code",
            "app",
            "role",
            "restriction",
        ]

        widgets = {
            "code": forms.TextInput(
                attrs={
                    "placeholder": "Código de la normativa",
                    "class": "form-control",
                    "minlength": "1",
                    "maxlength": "6",
                }
            ),
        }

    def clean(self):
        datos = self.cleaned_data
