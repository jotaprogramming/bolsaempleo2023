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


class UserGroupFormDelete(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserGroupFormDelete, self).__init__(*args, **kwargs)
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
