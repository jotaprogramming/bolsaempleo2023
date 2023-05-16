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
from django.utils.timezone import now
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
policy_title = _("Regulaciones")
policy_desc = _("Normativas de ejecución para grupos de usuarios")
rule_title = _("Reglas")
rule_desc = _(
    "Directrices que categorizan usuarios y permiten y/o restringen sus movimientos dentro del sistema"
)
user_title = _("Usuarios")
user_desc = _("Usuarios del sistema")
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
cv_title = _("Hoja de vida")
cv_desc = _("Llena tu hoja de vida para que las empresas puedan conocerte")

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
        form.instance.code = str(form.instance.code).upper()
        form.instance.group_name = str(form.instance.group_name).lower()

        objects = duplicate_usergroups(self, form)
        if objects > 0:
            warning_message(self.request, msg="El registro ya existe")
            return HttpResponseRedirect(reverse_lazy("users_app:usergroup_list"))
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("users_app:usergroup_list"))


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
        form.instance.code = str(form.instance.code).upper()
        form.instance.group_name = str(form.instance.group_name).lower()
        form.instance.updated_at = timezone.now()

        objects = duplicate_usergroups(self, form)
        if objects > 0:
            warning_message(self.request, msg="El registro ya existe")
            return HttpResponseRedirect(reverse_lazy("users_app:usergroup_list"))

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
        form.instance.code = str(form.instance.code).upper()
        form.instance.name = str(form.instance.name).lower()

        count = duplicate_restrictions(self, form)
        if count > 0:
            warning_message(self.request, msg="El registro ya existe")
            return HttpResponseRedirect(reverse_lazy("users_app:restriction_list"))
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
        count = duplicate_restrictions(self, form)
        form.instance.code = str(form.instance.code).upper()
        form.instance.name = str(form.instance.name).lower()
        form.instance.updated_at = timezone.now()

        if count > 0:
            warning_message(self.request, msg="El registro ya existe")
            return HttpResponseRedirect(reverse_lazy("users_app:restriction_list"))

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
        form.instance.code = str(form.instance.code).upper()
        form.instance.role_name = str(form.instance.role_name).lower()

        objects = duplicate_roles(self, form)
        if objects > 0:
            warning_message(self.request, msg="El registro ya existe")
            return HttpResponseRedirect(reverse_lazy("users_app:role_list"))

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
        form.instance.code = str(form.instance.code).upper()
        form.instance.role_name = str(form.instance.role_name).lower()
        form.instance.updated_at = timezone.now()

        objects = duplicate_roles(self, form)
        if objects > 0:
            warning_message(self.request, msg="El registro ya existe")
            return HttpResponseRedirect(reverse_lazy("users_app:role_list"))

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


# POLICIES
class PolicyList(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = UserGroupPolicies
    template_name = "policies/policy_list.html"
    paginate_by = 10

    def get_queryset(self):
        data = UserGroupPolicies.objects.get_nums()
        return data

    def get_context_data(self, **kwargs):
        context = super(PolicyList, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = policy_title
        context["description_view"] = policy_desc
        return context


class PolicyCreate(LoginRequiredMixin, generic.CreateView):
    login_url = "/login"
    model = UserGroupPolicies
    form_class = PolicyForm
    template_name = "policies/policy_create_modal.html"

    def get_success_url(self):
        success_message(self.request)
        return reverse_lazy("users_app:policy_list")

    def get_context_data(self, **kwargs):
        context = super(PolicyCreate, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = policy_title
        context["description_view"] = policy_desc
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("users_app:policy_list"))


class PolicyEditModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = UserGroupPolicies
    form_class = PolicyForm
    template_name = "policies/policy_update_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Registro actualizado satisfactoriamente")
        return reverse_lazy("users_app:policy_list")

    def get_context_data(self, **kwargs):
        context = super(PolicyEditModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = policy_title
        context["description_view"] = policy_desc
        return context

    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("users_app:policy_list"))


class PolicyDeleteModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = UserGroupPolicies
    form_class = FormDelete
    template_name = "policies/policy_delete_modal.html"

    def get_queryset(self):
        data = UserGroupPolicies.objects.order_by()
        return data

    def get_success_url(self):
        success_message(self.request, msg="Registro eliminado satisfactoriamente")
        return reverse_lazy("users_app:policy_list")

    def get_context_data(self, **kwargs):
        context = super(PolicyDeleteModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = policy_title
        context["description_view"] = policy_desc
        return context

    def form_valid(self, form):
        form.instance.deleted_at = timezone.now()
        return super().form_valid(form)


# USER RULES
class UserRulesList(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = UserRules
    template_name = "rules/rule_list.html"
    paginate_by = 10

    def get_queryset(self):
        data = UserRules.objects.order_by()
        return data

    def get_context_data(self, **kwargs):
        context = super(UserRulesList, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = rule_title
        context["description_view"] = rule_desc
        return context


class UserRulesCreate(LoginRequiredMixin, generic.CreateView):
    login_url = "/login"
    model = UserRules
    form_class = UserRuleForm
    template_name = "rules/rule_create_modal.html"

    def get_success_url(self):
        success_message(self.request)
        return reverse_lazy("users_app:rule_list")

    def get_context_data(self, **kwargs):
        context = super(UserRulesCreate, self).get_context_data(**kwargs)
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


class UserRulesEditModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = UserRules
    form_class = UserRuleForm
    template_name = "rules/rule_update_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Registro actualizado satisfactoriamente")
        return reverse_lazy("users_app:rule_list")

    def get_context_data(self, **kwargs):
        context = super(UserRulesEditModal, self).get_context_data(**kwargs)
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


class UserRulesDeleteModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = UserRules
    form_class = FormDelete
    template_name = "rules/rule_delete_modal.html"

    def get_queryset(self):
        data = UserRules.objects.order_by()
        return data

    def get_success_url(self):
        success_message(self.request, msg="Registro eliminado satisfactoriamente")
        return reverse_lazy("users_app:rule_list")

    def get_context_data(self, **kwargs):
        context = super(UserRulesDeleteModal, self).get_context_data(**kwargs)
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
    form_class = UserPassForm
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
        # usergroup = form.cleaned_data["usergroup"]
        # role = form.cleaned_data["role"]
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active,
        )
        # UserRules.objects.create(user=user, usergroup=usergroup, role=role)
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
    form_class = UserForm
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
        comgra = user.rule_user.filter(usergroup__code__in=["COM", "GRA"])
        admmod = user.rule_user.filter(usergroup__code__in=["MOD"]).filter(
            role__code__in=["ADM"]
        )
        memmod = user.rule_user.filter(usergroup__code__in=["MOD"]).filter(
            role__code__in=["MEM"]
        )
        if user.is_staff or admmod:
            return reverse_lazy("users_app:user_list")
        if comgra:
            return reverse_lazy("offers_app:bidding_panel")
        if memmod:
            return reverse_lazy("users_app:user_list")
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


# USER PROFILE
class UserProfileDetail(LoginRequiredMixin, generic.TemplateView):
    login_url = "/login"
    # model = UserProfile
    template_name = "userprofile/userprofile_detail.html"

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetail, self).get_context_data(**kwargs)
        username_param = self.kwargs.get("slug", "")

        try:
            # userprofile = UserProfile.objects.filter(user__username=username_param)
            obj = User.objects.get(username=username_param)
            context["object"] = obj

            userprofile = UserProfile.objects.filter(user=obj)
            if not userprofile:
                UserProfile.objects.create(user=obj)
            context["userprofile"] = userprofile

            # rules = UserRules.objects.filter(user__username=username_param)
            # context["rules"] = rules
        except Exception as ex:
            print("Error in <<get_context_data ~ UserProfileDetail>>: ", ex)
            pass

        context["app_title"] = "Perfil"
        context["title_view"] = "Detalle"
        context["initial"] = username_param[0]
        context["username"] = username_param
        context["profile"] = True
        context["company"] = User.objects.filter(
            username=username_param, rule_user__usergroup__code="COM"
        ).count()

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
        context["profile"] = True
        return context

    def form_valid(self, form):
        try:
            slug = self.kwargs.get("slug", "")
            form.instance.user = User.objects.get(username=slug)
            form.instance.email = normalize_email(form.instance.email)
            return super().form_valid(form)
        except Exception as exception:
            message = getattr(exception, "message", str(exception))
            error_message(self.request, msg=message, time=20000)
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
        context["fullname"] = User.objects.filter(username=slug).values()[0][
            "first_name"
        ]
        context["profile"] = True
        return context

    def form_valid(self, form):
        slug = self.kwargs.get("slug", "")
        # fullname = form.cleaned_data["avatar"]
        # fullname = form.cleaned_data["fullname"]
        # user.update(first_name=fullname)
        form.instance.updated_at = now()
        form.instance.email = normalize_email(form.instance.email)
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        slug = self.kwargs.get("slug", "")
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(
            reverse_lazy("users_app:userprofile_edit", args=[slug])
        )


# REGISTER
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
        return context

    def form_valid(self, form):
        # objects = duplicate_users(self, form)
        # if objects > 0:
        #     if (
        #         self.cleaned_data["username"] == "admin"
        #         or self.cleaned_data["username"] == "root"
        #     ):
        #         msg = _(f"Nombre de usuario no permitido")
        #     else:
        #         msg = _(f"El nombre de usuario ya existe")

        #     warning_message(self.request, msg=msg)
        #     return HttpResponseRedirect(reverse_lazy("home_app:register"))
        username = str(form.instance.username).lower()
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form
        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return self.render_to_response(ctx)


class RegisterStudentView(UserLoggedMixin, generic.FormView):
    model = User
    form_class = RegisterStudentForm
    template_name = "users/register_student.html"

    def get_success_url(self):
        success_message(
            self.request,
            "¡Bien hecho! Ahora solo queda esperar. Tus datos serán validados por nuestro equipo.",
            time=20000,
        )
        return reverse_lazy("users_app:login")

    def get_context_data(self, **kwargs):
        context = super(RegisterStudentView, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = student_register_desc
        context["desciption_view"] = register_title

        return context

    def form_valid(self, form):
        first_name = str(form.cleaned_data["first_name"]).upper()
        last_name = str(form.cleaned_data["last_name"]).upper()
        document_type = form.cleaned_data["document_type"]
        id_number = form.cleaned_data["id_number"]
        phone = form.cleaned_data["phone"]
        contact_email = form.cleaned_data["contact_email"]
        address = form.cleaned_data["address"]
        district = form.cleaned_data["district"]
        city = form.cleaned_data["city"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        try:
            last_name_split = last_name.split(" ")
            cod_name = f"{first_name[0]}{last_name_split[0]}"
            cod_name = format_diacritics(cod_name)
            last_id = User.objects.filter(username__icontains=cod_name).order_by("-id")
            user_id = int(last_id[0].id) if last_id.count() > 0 else 0
            username = f"{cod_name}{user_id + 1}".lower()

            usergroup = UserGroups.objects.get(code__icontains="GRA")
            role = Roles.objects.get(code__icontains="MEM")

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=False,
            )
            UserProfile.objects.create(
                user=user,
                document_type=document_type,
                id_number=id_number,
                phone=phone,
                email=contact_email,
                address=address,
                city=city,
                about_me="",
            )
            UserRules.objects.create(
                user=user,
                usergroup=usergroup,
                role=role,
            )
            return super().form_valid(form)
        except Exception as exception:
            message = "¡Oh no! Algo ocurrió. Por favor comuníquese con soporte para encontrar una solución"
            # message = getattr(exception, "message", str(exception))
            print(f"Error when registering the student: {exception}")
            error_message(self.request, msg=message)
            return HttpResponseRedirect(reverse_lazy("users_app:register_student"))


class RegisterCompanyView(UserLoggedMixin, generic.FormView):
    model = User
    form_class = RegisterCompanyForm
    template_name = "users/register_company.html"

    def get_success_url(self):
        success_message(
            self.request,
            "¡Bien hecho! Ahora solo queda esperar. Tus datos serán validados por nuestro equipo.",
            time=20000,
        )
        return reverse_lazy("users_app:login")

    def get_context_data(self, **kwargs):
        context = super(RegisterCompanyView, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = company_register_desc
        context["desciption_view"] = register_title

        return context

    def form_valid(self, form):
        try:
            # COMPANY
            name = form.cleaned_data["name"].upper()
            document_type = DocumentType.objects.get(acronym__icontains="NIT")
            id_number = form.cleaned_data["id_number"]
            phone = form.cleaned_data["phone"]
            contact_email = form.cleaned_data["contact_email"]
            address = form.cleaned_data["address"]
            district = form.cleaned_data["district"]
            city = form.cleaned_data["city"]
            # LEGAL REPRESENTATIVE
            rep_name = form.cleaned_data["rep_name"].upper()
            rep_document_type = form.cleaned_data["rep_document_type"]
            rep_id = form.cleaned_data["rep_id"]
            president = Specializations.objects.filter(
                name__icontains="REPRESENTANTE LEGAL"
            ).count()
            if president:
                rep_specialization = Specializations.objects.get(
                    name__icontains="REPRESENTANTE LEGAL"
                )
            else:
                rep_specialization = Specializations.objects.create(
                    name="REPRESENTANTE LEGAL"
                )
            # HUMAN RESOURCES
            humres_name = form.cleaned_data["humres_name"].upper()
            humres_document_type = form.cleaned_data["humres_document_type"]
            humres_id = form.cleaned_data["humres_id"]
            manager = Specializations.objects.filter(
                name__icontains="DIRECTOR DE RECURSOS HUMANOS"
            ).count()
            if manager:
                humres_specialization = Specializations.objects.get(
                    name__icontains="DIRECTOR DE RECURSOS HUMANOS"
                )
            else:
                humres_specialization = Specializations.objects.create(
                    name="DIRECTOR DE RECURSOS HUMANOS"
                )
            # USER
            username = form.instance.username.lower()
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            usergroup = UserGroups.objects.get(code__icontains="COM")
            role = Roles.objects.get(code__icontains="ADM")

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=False,
            )
            rep = Personnel(
                document_type=rep_document_type,
                id_number=rep_id,
                fullname=rep_name,
                specialization=rep_specialization,
            )
            humres = Personnel(
                document_type=humres_document_type,
                id_number=humres_id,
                fullname=humres_name,
                specialization=humres_specialization,
            )
            userprofile = UserProfile(
                user_id=user.id,
                document_type=document_type,
                id_number=id_number,
                phone=phone,
                email=contact_email,
                address=address,
                city=city,
                about_me="",
            )
            rule = UserRules(
                user=user,
                usergroup=usergroup,
                role=role,
            )
            company = Companies(
                name=name,
                userprofile=userprofile,
            )
            rep.save()
            humres.save()
            userprofile.save()
            rule.save()
            company.save()
            company.personnel.set([rep, humres])
        except Exception as exception:
            message = "¡Oh no! Algo ocurrió. Por favor comuníquese con soporte para encontrar una solución"
            # message = getattr(exception, "message", str(exception))
            print(f"Error when registering the company: {exception}")
            error_message(self.request, msg=message)
            return HttpResponseRedirect(reverse_lazy("users_app:register_company"))

        return super().form_valid(form)


class CredentialsRecoverView(generic.TemplateView):
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


# CURRICULUM VITAE
class CurriculumVitaeCreate(LoginRequiredMixin, generic.CreateView):
    login_url = "/login"
    model = CurriculumVitae
    form_class = CurriculumVitaeForm
    template_name = "curriculum/cv_create.html"

    def get_success_url(self):
        slug = self.kwargs.get("slug", "")
        cv = self.object

        # Education
        study_level_id = self.request.POST.get("study_level", "")
        academy = self.request.POST.get("academy", "")
        ac_start_date = self.request.POST.get("ac_start_date", "")
        ac_end_date = self.request.POST.get("ac_end_date", "")
        ac_currently = self.request.POST.get("ac_currently", "")

        ac_currently = True if ac_currently == "on" else False

        academic_institution = Entities(
            another_name=academy,
            start_date=ac_start_date,
            end_date=None if ac_currently else ac_end_date,
            currently=ac_currently,
        )
        academic_institution.save()

        education = Education(cv=cv, academy=academic_institution, level=study_level_id)
        education.save()

        # Languages
        lan_level = self.request.POST.get("lan_level", "")
        language_id = self.request.POST.get("language", "")

        perlan = PersonalLanguages(cv=cv, language_id=language_id, level=lan_level)
        perlan.save()

        # Company
        com_name = self.request.POST.get("company", "")
        com_start_date = self.request.POST.get("com_start_date", "")
        com_end_date = self.request.POST.get("com_end_date", "")
        com_currently = self.request.POST.get("com_currently", "")
        rating = self.request.POST.get("rating", "")
        performances = self.request.POST.get("performances", "")

        com_currently = True if com_currently == "on" else False

        company = None
        companies = Companies.objects.filter(name__icontains=com_name)
        if companies:
            company = companies.first()

        corporate_institution = Entities(
            company=company,
            another_name=None if company else com_name,
            start_date=com_start_date,
            end_date=None if com_currently else com_end_date,
            currently=com_currently,
        )
        corporate_institution.save()

        works = Works(
            cv=cv,
            company=corporate_institution,
            rating=rating,
            performances=performances,
        )
        works.save()

        success_message(
            self.request, msg="Tu hoja de vida fue añadida satisfactoriamente"
        )
        return reverse_lazy("users_app:userprofile", args=[slug])

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get("slug", "")
        context = super(CurriculumVitaeCreate, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = cv_title
        context["description_view"] = cv_desc
        context["username"] = slug
        context["datalist_company"] = Companies.objects.all()
        context["datalist_academy"] = Entities.objects.exclude(academy__in=[None])
        context["languages"] = Languages.objects.all()
        context["study_level"] = STUDY_LEVEL
        context["lan_level"] = LAN_LEVEL
        return context

    def form_valid(self, form):
        slug = self.kwargs.get("slug", "")
        try:
            userprofile = UserProfile.objects.get(user__username=slug)
            form.instance.userprofile = userprofile
        except Exception as ex:
            print(f"An exception occurred: {ex}")
            warning_message(self.request, msg=ex)
            return reverse_lazy("users_app:userprofile", args=[slug])
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        slug = self.kwargs.get("slug", "")
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return reverse_lazy("users_app:userprofile", args=[slug])


class CurriculumVitaeEdit(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = CurriculumVitae
    form_class = CurriculumVitaeForm
    template_name = "curriculum/cv_edit.html"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug", "")
        obj = self.model.objects.get(userprofile__user__username=slug)
        return obj

    def get_success_url(self):
        slug = self.kwargs.get("slug", "")
        cv = self.object

        # Company
        com_name = self.request.POST.get("company", "")
        com_start_date = self.request.POST.get("com_start_date", "")
        com_end_date = self.request.POST.get("com_end_date", "")
        com_currently = self.request.POST.get("com_currently", "")
        rating = self.request.POST.get("rating", "")
        performances = self.request.POST.get("performances", "")

        com_currently = True if com_currently == "on" else False

        performances = performances.replace("  ", " ")

        company = None
        companies = Companies.objects.filter(name__icontains=com_name)
        if companies:
            company = companies.first()

        works = Works.objects.filter(cv=cv)
        work = works.first()
        corporate_institution = Entities.objects.get(pk=work.company.pk)
        corporate_institution.company = company
        corporate_institution.another_name = None if company else com_name
        corporate_institution.start_date = com_start_date
        corporate_institution.end_date = None if com_currently else com_end_date
        corporate_institution.currently = com_currently
        corporate_institution.save(
            update_fields=[
                "company",
                "another_name",
                "start_date",
                "end_date",
                "currently",
            ]
        )

        work.company = corporate_institution
        work.rating = rating
        work.performances = performances
        work.save(update_fields=["company", "rating", "performances"])

        # Education
        study_level_id = self.request.POST.get("study_level", "")
        academy = self.request.POST.get("academy", "")
        ac_start_date = self.request.POST.get("ac_start_date", "")
        ac_end_date = self.request.POST.get("ac_end_date", "")
        ac_currently = self.request.POST.get("ac_currently", "")

        ac_currently = True if ac_currently == "on" else False

        # academic_institution = Entities(
        #     another_name=academy,
        #     start_date=ac_start_date,
        #     end_date=None if ac_currently else ac_end_date,
        #     currently=ac_currently,
        # )
        # academic_institution.save()

        educations = Education.objects.filter(cv=cv)
        education = educations.first()
        academic_institution = Entities.objects.get(pk=education.academy.pk)
        academic_institution.another_name = academy
        academic_institution.start_date = ac_start_date
        academic_institution.end_date = None if ac_currently else ac_end_date
        academic_institution.currently = ac_currently
        academic_institution.save(
            update_fields=[
                "another_name",
                "start_date",
                "end_date",
                "currently",
            ]
        )
        education.academy = academic_institution
        education.level = study_level_id
        education.save(
            update_fields=[
                "academy",
                "level",
            ]
        )

        # # Languages
        lan_level = self.request.POST.get("lan_level", "")
        language_id = self.request.POST.get("language", "")

        perlan = PersonalLanguages.objects.filter(cv=cv).first()
        perlan.language_id = language_id
        perlan.level = lan_level
        perlan.save(
            update_fields=[
                "language_id",
                "level",
            ]
        )

        success_message(
            self.request, msg="Tu hoja de vida fue actualizada satisfactoriamente"
        )
        return reverse_lazy("users_app:userprofile", args=[slug])

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get("slug", "")
        context = super(CurriculumVitaeEdit, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = cv_title
        context["description_view"] = cv_desc
        context["username"] = slug
        context["datalist_company"] = Companies.objects.all()
        context["datalist_academy"] = Entities.objects.exclude(academy__in=[None])
        context["languages"] = Languages.objects.all()
        context["study_level"] = STUDY_LEVEL
        context["lan_level"] = LAN_LEVEL
        return context

    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        slug = self.kwargs.get("slug", "")
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("users_app:userprofile", args=[slug]))


class CurriculumVitaeDeleteAttached(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = CurriculumVitae
    form_class = FormDelete
    template_name = "curriculum/cv_delete_attached.html"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug", "")
        obj = self.model.objects.get(userprofile__user__username=slug)
        return obj

    def get_success_url(self):
        slug = self.kwargs.get("slug", "")
        attached = self.object.attached
        if attached:
            attached.delete()

        success_message(
            self.request, msg="Hoja de vida adjunta eliminada satisfactoriamente"
        )
        return reverse_lazy("users_app:userprofile", args=[slug])

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get("slug", "")
        context = super(CurriculumVitaeDeleteAttached, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = cv_title
        context["description_view"] = cv_desc
        context["username"] = slug

        return context

    def form_valid(self, form):
        # form.instance.deleted_at = timezone.now()
        return super().form_valid(form)

class CurriculumVitaeAttach(LoginRequiredMixin, generic.CreateView):
    login_url = "/login"
    model = CurriculumVitae
    form_class = CurriculumVitaeAttachForm
    template_name = "curriculum/cv_attach.html"

    def get_success_url(self):
        slug = self.kwargs.get("slug", "")

        success_message(
            self.request, msg="Tu hoja de vida fue subida satisfactoriamente"
        )
        return reverse_lazy("users_app:userprofile", args=[slug])

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get("slug", "")
        context = super(CurriculumVitaeAttach, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = cv_title
        context["description_view"] = cv_desc
        context["username"] = slug
        return context

    def form_valid(self, form):
        slug = self.kwargs.get("slug", "")
        try:
            userprofile = UserProfile.objects.get(user__username=slug)
            form.instance.userprofile = userprofile
        except Exception as ex:
            print(f"An exception occurred: {ex}")
            warning_message(self.request, msg=ex)
            return reverse_lazy("users_app:userprofile", args=[slug])
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        slug = self.kwargs.get("slug", "")
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("users_app:userprofile", args=[slug]))
