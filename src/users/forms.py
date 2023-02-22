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
from users.models import *
from users.utils import *


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
        self.fields["user"].label = "Usuario"
        self.fields["app"].label = "Aplicación"
        self.fields["role"].label = "Rol"
        self.fields["restriction"].label = "Restricción"

    class Meta:
        model = Rules

        fields = [
            "user",
            "app",
            "role",
            "restriction",
        ]

        widgets = {
            "user": forms.Select(attrs={"class": "form-select"}),
        }


class UserForm(forms.ModelForm):
    repeat_pass = forms.CharField(
        label="Repetir Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirmar contraseña",
                "class": "form-control",
                "minlength": "8",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Usuario"
        self.fields["email"].label = "Correo electrónico"
        self.fields["password"].label = "Contraseña"
        self.fields["is_superuser"].label = "¿Es superusuario?"
        self.fields["is_superuser"].required = False
        self.fields["is_staff"].label = "¿Es administrativo?"
        self.fields["is_staff"].required = False
        self.fields["is_active"].label = "¿Es activo?"
        self.fields["is_active"].required = False

    class Meta:
        model = User

        fields = [
            "email",
            "username",
            "password",
            "repeat_pass",
            "is_superuser",
            "is_staff",
            "is_active",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Nombre de usuario",
                    "class": "form-control",
                    "minlength": "3",
                    "maxlength": "150",
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "placeholder": "Contraseña",
                    "class": "form-control",
                    "minlength": "8",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    
                    #"placeholder": "Correo electrónico",
                    "class": "form-control",
                }
            ),
            "is_superuser": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "is_staff": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean_repeat_pass(self):
        if self.cleaned_data["password"] != self.cleaned_data["repeat_pass"]:
            self.add_error("repeat_pass", "Contraseña incorrecta")


class UserFormUpdate(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserFormUpdate, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Usuario"
        self.fields["email"].label = "Correo electrónico"
        self.fields["is_superuser"].label = "¿Es superusuario?"
        self.fields["is_superuser"].required = False
        self.fields["is_staff"].label = "¿Es administrativo?"
        self.fields["is_staff"].required = False
        self.fields["is_active"].label = "¿Es activo?"
        self.fields["is_active"].required = False

    class Meta:
        model = User

        fields = [
            "email",
            "username",
            "is_superuser",
            "is_staff",
            "is_active",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Nombre de usuario",
                    "class": "form-control",
                    "minlength": "3",
                    "maxlength": "150",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    #"placeholder": "Correo electrónico",
                    "class": "form-control",
                }
            ),
            "is_superuser": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "is_staff": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("User"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "single-input",
                # "placeholder": _("User"),
            }
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "single-input", 
                # "placeholder": _("Password")
            }
        ),
    )


class RegisterForm(forms.ModelForm):
    repeat_pass = forms.CharField(
        label="Repetir Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                # "placeholder": "Repita la contraseña",
                "class": "single-input",
                "minlength": "8",
            }
        ),
    )
    email = forms.CharField(
        label=_("Email"),
        required= True,
        widget= forms.EmailInput(
            attrs={
                "class": "single-input",
                
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Usuario"
        self.fields["email"].label = "Correo electrónico"
        self.fields["password"].label = "Contraseña"

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password",
            "repeat_pass",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    # "placeholder": "Nombre de usuario",
                    "class": "single-input",
                    "minlength": "3",
                    "maxlength": "150",
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    # "placeholder": "Contraseña",
                    "class": "single-input",
                    "minlength": "8",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    # "placeholder": "Correo electrónico",
                    "class": "single-input",
                    "minlength": "3",
                    
                }
            ),
        }

    def clean(self):
        username = self.cleaned_data["username"]
        user_cache = User.objects.filter(username=username).count()
        if user_cache > 0:
            if username == 'admin' or username == 'root':
                self.add_error("username", _(f'Nombre de usuario no permitido'))
            else:
                self.add_error("username", _(f'El nombre de usuario ya existe'))

        if self.cleaned_data["password"] != self.cleaned_data["repeat_pass"]:
            self.add_error("repeat_pass", _(f'Contraseña inválida'))