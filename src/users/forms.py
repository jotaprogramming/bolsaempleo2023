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
from users.models import *
from users.utils import *

doctype_default = None
try:
    doctype_default = DocumentType.objects.get(acronym__icontains="CC")
except:
    pass


class UserGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserGroupForm, self).__init__(*args, **kwargs)
        self.fields["code"].label = "Código"
        self.fields["group_name"].label = "Nombre"
        self.fields["description"].label = "Descripción"

    class Meta:
        model = UserGroups

        fields = [
            "code",
            "group_name",
            "description",
        ]

        widgets = {
            "code": forms.TextInput(
                attrs={
                    "placeholder": "Código del grupo",
                    "class": "form-control",
                    "minlength": "1",
                    "maxlength": "50",
                }
            ),
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


# class PolicyForm(forms.ModelForm):
#     restriction = forms.ModelMultipleChoiceField(
#         queryset=Restrictions.objects.filter(deleted_at=None),
#         required=False,
#         label=_("Restricción"),
#         widget=forms.SelectMultiple(attrs={"class": "form-select"}),
#     )

#     app = forms.ModelMultipleChoiceField(
#         queryset=Apps.objects.filter(deleted_at=None),
#         required=True,
#         label=_("Aplicaciones"),
#         widget=forms.SelectMultiple(attrs={"class": "form-select"}),
#     )

#     def __init__(self, *args, **kwargs):
#         super(UserGroupForm, self).__init__(*args, **kwargs)
#         self.fields["usergroup"].label = "Grupo de usuarios"
#         self.fields["app"].label = "Aplicacion(es)"
#         self.fields["restriction"].label = "Descripción(es)"

#     class Meta:
#         model = UserGroupPolicies

#         fields = [
#             "usergroup",
#             "app",
#             "restriction",
#         ]

#         widgets = {
#             "usergroup": forms.Select(
#                 attrs={
#                     "class": "form-control",
#                 }
#             ),
#         }


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


class RoleForm(forms.ModelForm):
    restriction = forms.ModelMultipleChoiceField(
        queryset=Restrictions.objects.filter(deleted_at=None),
        required=False,
        label=_("Restricción"),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.fields["code"].label = "Código"
        self.fields["role_name"].label = "Nombre"
        self.fields["description"].label = "Descripción"

    class Meta:
        model = Roles

        fields = [
            "code",
            "role_name",
            "description",
            "restriction",
        ]

        widgets = {
            "code": forms.TextInput(
                attrs={
                    "placeholder": "Código del rol",
                    "class": "form-control",
                    "minlength": "1",
                    "maxlength": "50",
                }
            ),
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


class PolicyForm(forms.ModelForm):
    app = forms.ModelMultipleChoiceField(
        queryset=Apps.objects.filter(deleted_at=None),
        required=True,
        label=_("Aplicación"),
        widget=forms.SelectMultiple(
            attrs={"class": "form-select", "style": "height: 10rem"}
        ),
    )

    restriction = forms.ModelMultipleChoiceField(
        queryset=Restrictions.objects.filter(deleted_at=None),
        required=False,
        label=_("Restricción"),
        widget=forms.SelectMultiple(
            attrs={"class": "form-select", "style": "height: 10rem"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super(PolicyForm, self).__init__(*args, **kwargs)
        self.fields["usergroup"].label = "Grupo de Usuarios"
        self.fields["restriction"].label = "Restricción(es)"
        self.fields["app"].label = "Aplicación(es) (opcional)"

    class Meta:
        model = UserGroupPolicies

        fields = [
            "usergroup",
            "restriction",
            "app",
        ]

        widgets = {
            "usergroup": forms.Select(attrs={"class": "form-select"}),
        }


class UserRuleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserRuleForm, self).__init__(*args, **kwargs)
        self.fields["user"].label = "Usuario"
        self.fields["usergroup"].label = "Grupo"
        self.fields["role"].label = "Rol"

    class Meta:
        model = UserRules

        fields = [
            "user",
            "usergroup",
            "role",
        ]

        widgets = {
            "user": forms.Select(attrs={"class": "form-select"}),
            "usergroup": forms.Select(attrs={"class": "form-select"}),
            "role": forms.Select(attrs={"class": "form-select"}),
        }


class UserForm(forms.ModelForm):
    # usergroup = forms.ModelChoiceField(
    #     queryset=UserGroups.objects.all(),
    #     label=_("Grupo"),
    #     required=True,
    #     widget=forms.Select(attrs={"class": "form-select"}),
    # )
    # role = forms.ModelChoiceField(
    #     queryset=Roles.objects.all(),
    #     label=_("Rol"),
    #     required=True,
    #     widget=forms.Select(attrs={"class": "form-select"}),
    # )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
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
                    # "placeholder": "Correo electrónico",
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


class UserPassForm(UserForm):
    repeat_pass = forms.CharField(
        label=_("Repetir Contraseña"),
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
        super(UserPassForm, self).__init__(*args, **kwargs)
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
                    "placeholder": "Correo electrónico",
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
        label=_("Repetir Contraseña"),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                # "placeholder": "Repita la contraseña",
                "class": "single-input",
                "minlength": "8",
                "title": _("Repite la contraseña"),
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].label = "Usuario (opcional)"
        self.fields["first_name"].required = False
        self.fields["last_name"].label = "Apellidos (opcional)"
        self.fields["last_name"].required = False
        self.fields["username"].label = "Usuario"
        self.fields["email"].label = "Correo de registro"
        self.fields["email"].required = True
        self.fields["password"].label = "Contraseña"

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "repeat_pass",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "minlength": "1",
                    "maxlength": "150",
                    "title": _("Nombre del usuario"),
                },
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "minlength": "1",
                    "maxlength": "150",
                    "title": _("Apellidos del usuario"),
                },
            ),
            "username": forms.TextInput(
                attrs={
                    # "placeholder": "Nombre de usuario",
                    "class": "single-input",
                    "minlength": "3",
                    "maxlength": "150",
                    "title": _("Usuario"),
                },
            ),
            "password": forms.PasswordInput(
                attrs={
                    # "placeholder": "Contraseña",
                    "class": "single-input",
                    "minlength": "8",
                    "title": _("Contraseña"),
                },
            ),
            "email": forms.EmailInput(
                attrs={
                    # "placeholder": "Correo electrónico",
                    "class": "single-input",
                    "minlength": "3",
                    "title": _("Correo electrónico de registro"),
                },
            ),
        }

    # def clean_username_not_allowed(self):
    #     user_cache = User.objects.filter(username=self.cleaned_data["username"]).count()

    #     if user_cache > 0:
    #         if (
    #             self.cleaned_data["username"] == "admin"
    #             or self.cleaned_data["username"] == "root"
    #         ):
    #             self.add_error("username", _(f"Nombre de usuario no permitido"))
    #         else:
    #             self.add_error("username", _(f"El nombre de usuario ya existe"))

    def clean_repeat_pass(self):
        if self.cleaned_data["password"] != self.cleaned_data["repeat_pass"]:
            self.add_error("repeat_pass", _(f"Contraseña inválida"))


class RegisterCompanyForm(RegisterForm):
    # ------ Company
    name = forms.CharField(
        label=_("Razón social"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "single-input",
                "title": _("Nombre / razón social de la compañía"),
            }
        ),
    )
    id_number = forms.CharField(
        label=_("NIT"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "single-input",
                "title": _("Número de identificación tributario"),
            }
        ),
    )
    phone = forms.CharField(
        label=_("Teléfono"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "single-input",
                "title": _("Teléfono de contacto"),
            }
        ),
    )
    contact_email = forms.EmailField(
        label=_("Correo de contacto"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "single-input",
                "title": _("Correo electrónico de contacto"),
            }
        ),
    )
    address = forms.CharField(
        label=_("Dirección"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "single-input",
                "title": _("Dirección de la empresa"),
            }
        ),
    )
    district = forms.ModelChoiceField(
        queryset=Districts.objects.all(),
        label=_("Departamento"),
        required=True,
        widget=forms.Select(
            attrs={
                "class": "single-input",
                "title": _("Departamento donde se registró la empresa"),
            }
        ),
    )
    city = forms.ModelChoiceField(
        queryset=Cities.objects.all(),
        label=_("Ciudad"),
        required=True,
        widget=forms.Select(
            attrs={
                "class": "single-input  ",
                "title": _("Ciudad donde se registró la empresa"),
            }
        ),
    )
    # ------ Personnel
    # Legal representative
    rep_name = forms.CharField(
        max_length=100,
        label=_("Representante legal"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "single-input",
                "title": _("Nombre completo del representante legal"),
            }
        ),
    )
    rep_document_type = forms.ModelChoiceField(
        queryset=DocumentType.objects.all(),
        label=_("Tipo de documento"),
        required=True,
        widget=forms.Select(
            attrs={
                "class": "single-input rounded-end-0",
                "title": _("Tipo de documento del representante legal"),
                "style": "width: 40px !important; height: 40px !important; padding: .375rem 7px !important;",
            },
        ),
        initial=doctype_default,
    )
    rep_id = forms.CharField(
        max_length=15,
        label=_("Documento del Rep. Legal"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "single-input",
                "title": _("Número de identificación del representante legal"),
            }
        ),
    )
    # Human Resources
    humres_name = forms.CharField(
        max_length=100,
        label=_("Dir. Rec. Humanos"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "single-input",
                "title": _("Nombre del director de recursos humanos"),
            }
        ),
    )
    humres_document_type = forms.ModelChoiceField(
        queryset=DocumentType.objects.all(),
        label=_("Tipo de documento"),
        required=True,
        widget=forms.Select(
            attrs={
                "class": "single-input rounded-end-0",
                "title": _("Tipo de documento del director de recursos humanos"),
                "style": "width: 40px !important; height: 40px !important; padding: .375rem 7px !important;",
            }
        ),
        initial=doctype_default,
    )
    humres_id = forms.CharField(
        max_length=15,
        label=_("Documento del Dir. de RRHH"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "single-input",
                "title": _("Número de documento del director de recursos humanos"),
            }
        ),
    )


class RegisterStudentForm(RegisterForm):
    # avatar = forms.FileField(
    #     label=_("Foto de perfil"),
    #     allow_empty_file=False,
    #     required=False,
    #     widget=forms.FileInput(
    #         attrs={
    #             "class": "form-control",
    #         }
    #     ),
    # )
    document_type = forms.ModelChoiceField(
        queryset=DocumentType.objects.all(),
        label=_("Tipo de documento"),
        required=True,
        widget=forms.Select(
            attrs={
                "class": "single-input",
            }
        ),
        initial=doctype_default,
    )
    id_number = forms.CharField(
        label=_("Número de identidad"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "single-input",
            }
        ),
    )
    phone = forms.CharField(
        label=_("Teléfono"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "single-input",
            }
        ),
    )
    contact_email = forms.EmailField(
        label=_("Correo electróncio de contacto"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "single-input",
            }
        ),
    )
    address = forms.CharField(
        label=_("Dirección"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "single-input",
            }
        ),
    )
    district = forms.ModelChoiceField(
        queryset=Districts.objects.all(),
        label=_("Departamento"),
        required=True,
        widget=forms.Select(
            attrs={
                "class": "single-input",
            }
        ),
    )
    city = forms.ModelChoiceField(
        queryset=Cities.objects.all(),
        label=_("Ciudad"),
        required=True,
        widget=forms.Select(
            attrs={
                "class": "single-input",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["username"].required = False
        self.fields["username"].label = "Usuario"
        self.fields["email"].label = "Correo electrónico"
        self.fields["email"].required = True
        self.fields["password"].label = "Contraseña"


class UserProfileModelForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_("Nombre"),
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "single-input",
                "title": _("Nombre"),
            }
        ),
    )
    last_name = forms.CharField(
        label=_("Nombre"),
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "single-input",
                "title": _("Apellidos"),
            }
        ),
    )
    district = forms.ModelChoiceField(
        queryset=Districts.objects.all(),
        label=_("Departamento"),
        required=True,
        widget=forms.Select(
            attrs={
                "class": "single-input",
                "title": _("Departamento donde se registró la empresa"),
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super(UserProfileModelForm, self).__init__(*args, **kwargs)
        self.fields["avatar"].label = "Avatar"
        self.fields["web"].label = "Web"
        self.fields["document_type"].label = "Tipo de documento"
        self.fields["id_number"].label = "Número de identificación"
        self.fields["phone"].label = "Teléfono"
        self.fields["email"].label = "Correo electrónico"
        self.fields["address"].label = "Dirección"
        self.fields["city"].label = "Ciudad"
        self.fields["about_me"].label = "Sobre mí"
        self.fields["avatar"].required = False
        self.fields["web"].required = False
        self.fields["document_type"].required = True
        self.fields["id_number"].required = True
        self.fields["phone"].required = True
        self.fields["email"].required = True
        self.fields["address"].required = False
        self.fields["city"].required = True
        self.fields["about_me"].required = False

    class Meta:
        model = UserProfile

        fields = [
            "avatar",
            "web",
            "document_type",
            "id_number",
            "phone",
            "email",
            "address",
            "city",
            "about_me",
        ]

        widgets = {
            "avatar": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "title": _("Subir foto de perfil"),
                },
            ),
            "web": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "minlength": "1",
                    "title": _("Página web o red social"),
                }
            ),
            "document_type": forms.Select(
                attrs={
                    "class": "single-input rounded-end-0",
                    "title": _("Tipo de documento"),
                    "style": "width: 40px !important; height: 40px !important; padding: .375rem 7px !important;",
                },
            ),
            "id_number": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "title": _("Número de documento"),
                },
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "title": _("Número de teléfono (celular o fijo)"),
                },
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "single-input",
                    "title": _("Correo electrónico"),
                },
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "title": _("Dirección"),
                },
            ),
            "city": forms.Select(
                attrs={
                    "class": "single-input",
                    "title": _("Ciudad"),
                },
            ),
            "about_me": forms.Textarea(
                attrs={
                    "class": "form-control resize-n",
                    "minlength": "1",
                    "title": _("Sobre mí"),
                }
            ),
        }
