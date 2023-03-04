# PYTHON MODULES
from datetime import datetime
import json

# DJANGO MODULES
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse, resolve
from django.views import generic
from django.db import IntegrityError
from django.conf import settings
from django.db.models import (
    Q,
    F,
    Count,
    CharField,
    DecimalField,
    Value,
    Sum,
    Avg,
    Min,
    Max,
)
from django.utils.translation import gettext as _

# EXTRA MODULES
import sweetify

# PROJECT MODULES
from users.forms import *
from users.models import *
from core.utils import *
from core.middlewares import UserLoggedMixin
from users.utils import *
from jobboard.utils import *

# PROJECT FORMS

# GLOBAL VARIABLES
app_title = _("Usuarios")
usergroup_title = _("Grupos de usuarios")
usergroup_desc = _("Conjunto de usuarios que comparten un mismo propósito")
restriction_title = _("Restricciones")
restriction_desc = _("Todo tipo de acciones prohibidas para los usuarios")
app_view_title = _("Aplicaciones")
app_view_desc = _("Módulos del sistema")
role_title = _("Roles")
role_desc = _("Función que un usuario desempeña dentro del sistema")
rule_title = _("Reglas")
rule_desc = _("Serie de normativas que deben cumplir los usuarios del sistema")
user_title = _("Usuarios")
user_desc = _("Actores del sistema")
userprofile_title = _("Perfiles de usuario")
userprofile_desc = _("Perfiles de usuario del sistema")
login_title = _("Ingresar")
login_desc = _("Inicio de sesión")
register_title = _("Registro")
register_desc = _("Registrarse")
register_choices_desc = _("Registrarse")
register_choices_title = _("Seleccion")
account_already = _("si ya dispone de Usuario y Contraseña")
student_register_desc = _("Registro Estudiantes")
company_register_desc = _("Registro Empresas")
recover_title = _("Recuperar Credenciales")

# Create your views here.


# USER GROUPS
class UserGroupList(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = UserGroups
    template_name = "usergroups/usergroup_list.html"
    paginate_by = 10

    def get_queryset(self):
        data = UserGroups.objects.all().order_by("id")
        return data

    def get_context_data(self, **kwargs):
        context = super(UserGroupList, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = usergroup_title
        context["description_view"] = usergroup_desc
        return context


class UserGroupCreate(LoginRequiredMixin, generic.CreateView):
    login_url = "/login"
    model = UserGroups
    form_class = UserGroupForm
    template_name = "usergroups/usergroup_create_modal.html"

    def get_success_url(self):
        success_message(self.request)
        return reverse_lazy("users_app:usergroup_list")

    def get_context_data(self, **kwargs):
        context = super(UserGroupCreate, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = usergroup_title
        context["description_view"] = usergroup_desc
        return context

    def form_valid(self, form):
        objects = duplicate_usergroups(self, form)
        if objects > 0:
            warning_message(self.request, msg="El registro ya existe")
            return HttpResponseRedirect(reverse_lazy("users_app:usergroup_list"))
        form.instance.group_name = str(form.instance.group_name).lower()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return self.render_to_response(ctx)


class UserGroupEditModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = UserGroups
    form_class = UserGroupForm
    template_name = "usergroups/usergroup_update_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Registro actualizado satisfactoriamente")
        return reverse_lazy("users_app:usergroup_list")

    def get_context_data(self, **kwargs):
        context = super(UserGroupEditModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = usergroup_title
        context["description_view"] = usergroup_desc
        return context

    def form_valid(self, form):
        objects = duplicate_usergroups(self, form)
        if objects > 0:
            warning_message(self.request, msg="El registro ya existe")
            return HttpResponseRedirect(reverse_lazy("users_app:usergroup_list"))

        form.instance.group_name = str(form.instance.group_name).lower()
        form.instance.updated_at = timezone.now()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return self.render_to_response(ctx)


class UserGroupDeleteModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = UserGroups
    form_class = FormDelete
    template_name = "usergroups/usergroup_delete_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Registro eliminado satisfactoriamente")
        return reverse_lazy("users_app:usergroup_list")

    def get_context_data(self, **kwargs):
        context = super(UserGroupDeleteModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = usergroup_title
        context["description_view"] = usergroup_desc
        return context

    def form_valid(self, form):
        form.instance.deleted_at = timezone.now()
        return super().form_valid(form)


# RESTRICTIONS


class RestrictionList(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = Restrictions
    template_name = "restrictions/restriction_list.html"
    paginate_by = 10

    def get_queryset(self):
        data = Restrictions.objects.all().order_by("id")
        return data

    def get_context_data(self, **kwargs):
        context = super(RestrictionList, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = restriction_title
        context["description_view"] = restriction_desc
        return context


class RestrictionCreate(LoginRequiredMixin, generic.CreateView):
    login_url = "/login"
    model = Restrictions
    form_class = RestrictionForm
    template_name = "restrictions/restriction_create_modal.html"

    def get_success_url(self):
        success_message(self.request)
        return reverse_lazy("users_app:restriction_list")

    def get_context_data(self, **kwargs):
        context = super(RestrictionCreate, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = restriction_title
        context["description_view"] = restriction_desc
        return context

    def form_valid(self, form):
        # count_code, count_name = duplicate_restrictions(self, form)
        # if count_code > 0 or count_name > 0:
        #     warning_message(self.request, msg="El registro ya existe")
        #     return HttpResponseRedirect(reverse_lazy("users_app:restriction_list"))
        form.instance.code = str(form.instance.code).upper()
        form.instance.name = str(form.instance.name).lower()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("users_app:restriction_list"))


class RestrictionEditModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Restrictions
    form_class = RestrictionForm
    template_name = "restrictions/restriction_update_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Registro actualizado satisfactoriamente")
        return reverse_lazy("users_app:restriction_list")

    def get_context_data(self, **kwargs):
        context = super(RestrictionEditModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = restriction_title
        context["description_view"] = restriction_desc
        return context

    def form_valid(self, form):
        # count_code, count_name = duplicate_restrictions(self, form)
        # if count_code > 0 or count_name > 0:
        #     warning_message(self.request, msg="El registro ya existe")
        #     return HttpResponseRedirect(reverse_lazy("users_app:restriction_list"))

        form.instance.code = str(form.instance.code).upper()
        form.instance.name = str(form.instance.name).lower()
        form.instance.updated_at = timezone.now()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("users_app:restriction_list"))


class RestrictionDeleteModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Restrictions
    form_class = FormDelete
    template_name = "restrictions/restriction_delete_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Registro eliminado satisfactoriamente")
        return reverse_lazy("users_app:restriction_list")

    def get_context_data(self, **kwargs):
        context = super(RestrictionDeleteModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = restriction_title
        context["description_view"] = restriction_desc
        return context

    def form_valid(self, form):
        form.instance.deleted_at = timezone.now()
        return super().form_valid(form)


# APPS
class AppList(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = Apps
    template_name = "apps/app_list.html"
    paginate_by = 10

    def set_urls_in_db(self):
        """
        It takes a list of dictionaries, each dictionary containing a name and route, and saves them to
        the database
        """
        urls = get_url_names()

        for url in urls:
            objects = Apps.objects.all().order_by("id")
            f_objects = objects.filter(
                name__exact=url["name"], route__exact=url["route"]
            )
            if not f_objects:
                name_cache = objects.filter(name__exact=url["name"])
                if name_cache:
                    name_cache.update(route=url["route"], updated_at=timezone.now())
                    continue
                else:
                    route_cache = objects.filter(route__exact=url["route"])
                    if route_cache:
                        route_cache.update(name=url["name"], updated_at=timezone.now())
                        continue
                app = Apps(name=url["name"], route=url["route"], description="App")
                app.save()

    def get_queryset(self):
        data = Apps.objects.all().order_by("id")
        return data

    def get_context_data(self, **kwargs):
        context = super(AppList, self).get_context_data(**kwargs)

        self.set_urls_in_db()
        context["app_title"] = app_title
        context["title_view"] = app_view_title
        context["description_view"] = app_view_desc
        return context


class AppEditModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Apps
    form_class = AppForm
    template_name = "apps/app_update_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Registro actualizado satisfactoriamente")
        return reverse_lazy("users_app:app_list")

    def get_context_data(self, **kwargs):
        context = super(AppEditModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = app_view_title
        context["description_view"] = app_view_desc
        return context

    def form_valid(self, form):
        # count_name, count_route = duplicate_apps(self, form)
        # if count_name > 0 or count_route > 0:
        #     warning_message(self.request, msg="El registro ya existe")
        #     return HttpResponseRedirect(reverse_lazy("users_app:app_list"))

        form.instance.updated_at = timezone.now()
        return super().form_valid(form)


# ROLES
class RoleList(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = Roles
    template_name = "roles/role_list.html"
    paginate_by = 10

    def get_queryset(self):
        data = Roles.objects.all().order_by("id")
        return data

    def get_context_data(self, **kwargs):
        context = super(RoleList, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = role_title
        context["description_view"] = role_desc
        return context


class RoleCreate(LoginRequiredMixin, generic.CreateView):
    login_url = "/login"
    model = Roles
    form_class = RoleForm
    template_name = "roles/role_create_modal.html"

    def get_success_url(self):
        success_message(self.request)
        return reverse_lazy("users_app:role_list")

    def get_context_data(self, **kwargs):
        context = super(RoleCreate, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = role_title
        context["description_view"] = role_desc
        return context

    def form_valid(self, form):
        # objects = duplicate_roles(self, form)
        # if objects > 0:
        #     warning_message(self.request, msg="El registro ya existe")
        #     return HttpResponseRedirect(reverse_lazy("users_app:role_list"))

        form.instance.role_name = str(form.instance.role_name).lower()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("users_app:role_list"))


class RoleEditModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Roles
    form_class = RoleForm
    template_name = "roles/role_update_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Registro actualizado satisfactoriamente")
        return reverse_lazy("users_app:role_list")

    def get_context_data(self, **kwargs):
        context = super(RoleEditModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = role_title
        context["description_view"] = role_desc
        return context

    def form_valid(self, form):
        # objects = duplicate_roles(self, form)
        # if objects > 0:
        #     warning_message(self.request, msg="El registro ya existe")
        #     return HttpResponseRedirect(reverse_lazy("users_app:role_list"))

        form.instance.role_name = str(form.instance.role_name).lower()
        form.instance.updated_at = timezone.now()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("users_app:role_list"))


class RoleDeleteModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Roles
    form_class = FormDelete
    template_name = "roles/role_delete_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Registro eliminado satisfactoriamente")
        return reverse_lazy("users_app:role_list")

    def get_context_data(self, **kwargs):
        context = super(RoleDeleteModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = role_title
        context["description_view"] = role_desc
        return context

    def form_valid(self, form):
        form.instance.deleted_at = timezone.now()
        return super().form_valid(form)


# RULES
class RuleList(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = Rules
    template_name = "rules/rule_list.html"
    paginate_by = 10

    def get_queryset(self):
        data = Rules.objects.get_nums()
        return data

    def get_context_data(self, **kwargs):
        context = super(RuleList, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = rule_title
        context["description_view"] = rule_desc
        return context


class RuleCreate(LoginRequiredMixin, generic.CreateView):
    login_url = "/login"
    model = Rules
    form_class = RuleForm
    template_name = "rules/rule_create_modal.html"

    def get_success_url(self):
        success_message(self.request)
        return reverse_lazy("users_app:rule_list")

    def get_context_data(self, **kwargs):
        context = super(RuleCreate, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = rule_title
        context["description_view"] = rule_desc
        return context

    def form_valid(self, form):
        # objects = duplicate_rules(self, form)
        # if objects > 0:
        #     duplicate_message(self.request)
        #     return HttpResponseRedirect(reverse_lazy("users_app:rule_list"))
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("users_app:rule_list"))


class RuleEditModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Rules
    form_class = RuleForm
    template_name = "rules/rule_update_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Registro actualizado satisfactoriamente")
        return reverse_lazy("users_app:rule_list")

    def get_context_data(self, **kwargs):
        context = super(RuleEditModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = rule_title
        context["description_view"] = rule_desc
        return context

    def form_valid(self, form):
        # objects = duplicate_rules(self, form)
        # if objects > 0:
        #     duplicate_message(self.request)
        #     return HttpResponseRedirect(reverse_lazy("users_app:rule_list"))
        form.instance.updated_at = timezone.now()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("users_app:rule_list"))


class RuleDeleteModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Rules
    form_class = FormDelete
    template_name = "rules/rule_delete_modal.html"

    def get_queryset(self):
        data = Rules.objects.get_nums()
        return data

    def get_success_url(self):
        success_message(self.request, msg="Registro eliminado satisfactoriamente")
        return reverse_lazy("users_app:rule_list")

    def get_context_data(self, **kwargs):
        context = super(RuleDeleteModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = rule_title
        context["description_view"] = rule_desc
        return context

    def form_valid(self, form):
        form.instance.deleted_at = timezone.now()
        return super().form_valid(form)


# USERS
class UserList(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = User
    template_name = "users/user_list.html"
    paginate_by = 10

    def get_queryset(self):
        data = User.objects.all().order_by("id")
        return data

    def get_context_data(self, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = user_title
        context["description_view"] = user_desc
        return context


class UserCreate(LoginRequiredMixin, generic.FormView):
    login_url = "/login"
    model = User
    form_class = UserForm
    template_name = "users/user_create_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Usuario creado satisfactoriamente")
        return reverse_lazy("users_app:user_list")

    def get_context_data(self, **kwargs):
        context = super(UserCreate, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = user_title
        context["description_view"] = user_desc
        return context

    def form_valid(self, form):
        # objects = duplicate_users(self, form)
        # if objects > 0:
        #     warning_message(
        #         self.request, msg="El nombre de usuario ingresado ya está en uso"
        #     )
        #     return HttpResponseRedirect(reverse_lazy("users_app:user_list"))
        username = str(form.instance.username).lower()
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        is_superuser = form.cleaned_data["is_superuser"]
        is_staff = form.cleaned_data["is_staff"]
        is_active = form.cleaned_data["is_active"]
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active,
        )
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("users_app:user_list"))


class UserEditModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = User
    form_class = UserFormUpdate
    template_name = "users/user_update_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Registro actualizado satisfactoriamente")
        return reverse_lazy("users_app:user_list")

    def get_context_data(self, **kwargs):
        context = super(UserEditModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = user_title
        context["description_view"] = user_desc
        return context

    def form_valid(self, form):
        # objects = duplicate_users(self, form)
        # if objects > 0:
        #     warning_message(
        #         self.request, msg="El nombre de usuario ingresado ya está en uso"
        #     )
        #     return HttpResponseRedirect(reverse_lazy("users_app:user_list"))
        form.instance.username = str(form.instance.username).lower()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("users_app:user_list"))


class UserDeleteModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = User
    form_class = FormDelete
    template_name = "users/user_delete_modal.html"

    def get_queryset(self):
        data = User.objects.all().order_by("id")
        return data

    def get_success_url(self):
        success_message(self.request, msg="Registro eliminado satisfactoriamente")
        return reverse_lazy("users_app:user_list")

    def get_context_data(self, **kwargs):
        context = super(UserDeleteModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = user_title
        context["description_view"] = user_desc
        return context

    def form_valid(self, form):
        form.instance.is_active = False
        return super().form_valid(form)


class UserLogin(UserLoggedMixin, generic.FormView):
    model = User
    form_class = LoginForm
    template_name = "users/login.html"

    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            return reverse_lazy("users_app:user_list")
        else:
            return reverse_lazy("home_app:home_page")

    def get_context_data(self, **kwargs):
        context = super(UserLogin, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = login_title
        context["description_view"] = login_desc
        context[
            "image_url"
        ] = "core/assets/img/jess-bailey-mexeVPlTB6k-unsplash-compressed.jpg"
        context["image_alt"] = "jess-bailey-mexeVPlTB6k-unsplash"
        context[
            "graduate_text"
        ] = "Para estudiantes y egresados de Ingenieria de Sistemas"
        context["company_text"] = "Para empresas en busca de grandes Talentos"
        return context

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(
            username=username,
            password=password,
        )
        login(self.request, user)
        return super().form_valid(form)


class UserLogout(generic.View):
    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(reverse("users_app:login"))


class RegisterView(UserLoggedMixin, generic.FormView):
    model = User
    form_class = RegisterForm
    template_name = "users/register.html"

    def get_success_url(self):
        success_message(self.request)
        return reverse_lazy("users_app:login")

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = register_title
        context["description_view"] = register_desc
        context["account_view"] = account_already
        # context["img_url"] = 'core/assets/img/img.jpg'
        return context

    def form_valid(self, form):
        objects = duplicate_users(self, form)
        if objects > 0:
            if (
                self.cleaned_data["username"] == "admin"
                or self.cleaned_data["username"] == "root"
            ):
                msg = _(f"Nombre de usuario no permitido")
            else:
                msg = _(f"El nombre de usuario ya existe")

            warning_message(self.request, msg=msg)
            return HttpResponseRedirect(reverse_lazy("home_app:register"))
        try:
            username = str(form.instance.username).lower()
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            return super().form_valid(form)
        except Exception as exception:
            error_message(self.request)
            print(" ")
            print(exception)
            return HttpResponseRedirect(reverse_lazy("home_app:register"))

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form
        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return self.render_to_response(ctx)


# USER PROFILE


class UserProfileDetail(LoginRequiredMixin, generic.TemplateView):
    login_url = "/login"
    model = UserProfile
    template_name = "userprofile/userprofile_detail.html"

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetail, self).get_context_data(**kwargs)
        username_param = self.kwargs.get("slug", "")
        try:
            obj = UserProfile.objects.get(user__username=username_param)
            username = obj.user.username
            about_me = obj.about_me
            alias = obj.name or username
            context["object"] = obj
            context["title_view"] = alias
            context["description_view"] = about_me
        except:
            pass
        context["app_title"] = app_title
        context["username"] = username_param
        return context


class UserProfileCreate(LoginRequiredMixin, generic.CreateView):
    login_url = "/login"
    model = UserProfile
    form_class = UserProfileModelForm
    template_name = "userprofile/userprofile_add.html"

    def get_success_url(self):
        slug = self.kwargs.get("slug", "")
        success_message(self.request)
        return reverse_lazy("users_app:userprofile", args=[slug])

    def get_context_data(self, **kwargs):
        context = super(UserProfileCreate, self).get_context_data(**kwargs)
        slug = self.kwargs.get("slug", "")

        context["app_title"] = app_title
        context["title_view"] = "Perfil"
        context["description_view"] = f"@{slug}"
        context["username"] = slug
        return context

    def form_valid(self, form):
        slug = self.kwargs.get("slug", "")
        try:
            user = User.objects.get(username=slug)
            form.instance.email = normalize_email(form.instance.email)
            form.instance.user_id = user.id
            return super().form_valid(form)
        except Exception as exception:
            message = getattr(exception, "message", list(exception))
            error_message(self.request, msg=message)
            return HttpResponseRedirect(
                reverse_lazy("users_app:userprofile_add", args=[slug])
            )

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form
        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return self.render_to_response(ctx)


class UserProfileEdit(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = UserProfile
    form_class = UserProfileModelForm
    template_name = "userprofile/userprofile_edit.html"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug", "")
        obj = UserProfile.objects.get(user__username=slug)
        return obj

    def get_success_url(self):
        slug = self.kwargs.get("slug", "")
        success_message(self.request, msg="Registro actualizado satisfactoriamente")
        return reverse_lazy("users_app:userprofile", args=[slug])

    def get_context_data(self, **kwargs):
        context = super(UserProfileEdit, self).get_context_data(**kwargs)
        slug = self.kwargs.get("slug", "")

        context["app_title"] = app_title
        context["title_view"] = "Perfil"
        context["description_view"] = f"@{slug}"
        context["username"] = slug
        return context

    def form_valid(self, form):
        slug = self.kwargs.get("slug", "")
        try:
            form.instance.updated_at = datetime.now()
            form.instance.email = normalize_email(form.instance.email)
            return super().form_valid(form)
        except Exception as exception:
            message = getattr(exception, "message", list(exception))
            error_message(self.request, msg=message)
            return HttpResponseRedirect(
                reverse_lazy("users_app:userprofile_edit", args=[slug])
            )

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(
            reverse_lazy(
                "users_app:userprofile_edit", args=[self.request.user.username]
            )
        )


# ----------------------------------------------


class PreRegisterView(UserLoggedMixin, generic.TemplateView):
    # selection_url = "/register_choices"
    template_name = "users/selection_register.html"

    def get_context_data(self, **kwargs):
        context = super(PreRegisterView, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = register_choices_title
        context["description_view"] = register_choices_desc
        context["account_view"] = account_already
        context[
            "image_url"
        ] = "core/assets/img/jess-bailey-mexeVPlTB6k-unsplash-compressed.jpg"
        context["image_alt"] = "jess-bailey-mexeVPlTB6k-unsplash"
        context[
            "graduate_text"
        ] = "Para estudiantes y egresados de Ingenieria de Sistemas"
        context["company_text"] = "Para empresas en busca de grandes Talentos"

        return context


class RegisterStudentView(UserLoggedMixin, generic.TemplateView):
    model = User
    form_class = RegisterForm
    # student_register_url = "/student_register"
    template_name = "users/register_student.html"

    def get_context_data(self, **kwargs):
        context = super(RegisterStudentView, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = student_register_desc
        context["desciption_view"] = register_title

        return context


class RegisterCompanyView(UserLoggedMixin, generic.TemplateView):
    model = User
    form_class = RegisterForm
    # company_register_url = "/company_register"
    template_name = "users/register_company.html"

    def get_context_data(self, **kwargs):
        context = super(RegisterCompanyView, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = company_register_desc
        context["desciption_view"] = register_title

        return context


class CredentialsRecoverView(UserLoggedMixin, generic.TemplateView):
    # credentials_recover_url = "/credentials_recover"
    template_name = "users/credentials_recover.html"

    def get_context_data(self, **kwargs):
        context = super(CredentialsRecoverView, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = recover_title
        context[
            "image_url"
        ] = "core/assets/img/jess-bailey-mexeVPlTB6k-unsplash-compressed.jpg"
        context["image_alt"] = "jess-bailey-mexeVPlTB6k-unsplash"
        context[
            "graduate_text"
        ] = "Para estudiantes y egresados de Ingenieria de Sistemas"
        context["company_text"] = "Para empresas en busca de grandes Talentos"
        return context


# ----------------------------------------------------
