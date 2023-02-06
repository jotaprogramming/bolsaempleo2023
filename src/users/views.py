# PYTHON MODULES
from datetime import datetime
import json

# DJANGO MODULES
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.db import IntegrityError
from django.conf import settings

# EXTRA MODULES
import sweetify

# PROJECT MODULES
from users.forms import *
from users.models import *
from core.utils import *
from users.utils import *
from jobboard.utils import *

# PROJECT FORMS

# GLOBAL VARIABLES
app_title = "Usuarios"
usergroup_title = "Grupos de usuarios"
usergroup_desc = "Conjunto de usuarios que comparten un mismo propósito"
restriction_title = "Restricciones"
restriction_desc = "Todo tipo de acciones prohibidas para los usuarios"
app_view_title = "Aplicaciones"
app_view_desc = "Módulos del sistema"


# Create your views here.


# USER GROUPS
class UserGroupList(generic.ListView):
    # login_url = "/login"
    model = UserGroups
    template_name = "usergroups/usergroup_list.html"
    paginate_by = 25

    def get_queryset(self):
        data = UserGroups.objects.all().order_by("id")
        return data

    def get_context_data(self, **kwargs):
        context = super(UserGroupList, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = usergroup_title
        context["description_view"] = usergroup_desc
        return context


class UserGroupCreate(generic.CreateView):
    # login_url = "/login"
    model = UserGroups
    form_class = UserGroupForm
    template_name = "usergroups/usergroup_create_modal.html"

    def get_success_url(self):
        created_message(self.request)
        return reverse_lazy("users_app:usergroup_list")

    def get_context_data(self, **kwargs):
        context = super(UserGroupCreate, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = usergroup_title
        context["description_view"] = usergroup_desc
        return context

    def form_valid(self, form):
        objects = diplicate_usergroups(self, form)
        if objects > 0:
            duplicate_message(self.request)
            return HttpResponseRedirect(reverse_lazy("users_app:usergroup_list"))
        try:
            return super().form_valid(form)
        except Exception as exception:
            error_message(self.request)
            print(" ")
            print(exception)
            return HttpResponseRedirect(reverse_lazy("users_app:usergroup_list"))

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        form_invalid_message(self.request)
        return self.render_to_response(ctx)


class UserGroupEditModal(generic.UpdateView):
    # login_url = '/login'
    model = UserGroups
    form_class = UserGroupForm
    template_name = "usergroups/usergroup_update_modal.html"

    def get_success_url(self):
        updated_message(self.request)
        return reverse_lazy("users_app:usergroup_list")

    def get_context_data(self, **kwargs):
        context = super(UserGroupEditModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = usergroup_title
        context["description_view"] = usergroup_desc
        return context

    def form_valid(self, form):
        objects = diplicate_usergroups(self, form)
        if objects > 0:
            duplicate_message(self.request)
            return HttpResponseRedirect(reverse_lazy("users_app:usergroup_list"))
        try:
            form.instance.updated_at = datetime.now()
            return super().form_valid(form)
        except Exception as exception:
            error_message(self.request)
            print(" ")
            print(exception)
            return HttpResponseRedirect(reverse_lazy("users_app:usergroup_list"))

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        form_invalid_message(self.request)
        return self.render_to_response(ctx)


class UserGroupDeleteModal(generic.UpdateView):
    # login_url = '/login'
    model = UserGroups
    form_class = FormDelete
    template_name = "usergroups/usergroup_delete_modal.html"

    def get_success_url(self):
        deleted_message(self.request)
        return reverse_lazy("users_app:usergroup_list")

    def get_context_data(self, **kwargs):
        context = super(UserGroupDeleteModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = usergroup_title
        context["description_view"] = usergroup_desc
        return context

    def form_valid(self, form):
        try:
            form.instance.deleted_at = datetime.now()
            return super().form_valid(form)
        except Exception as exception:
            error_message(self.request)
            print(" ")
            print(exception)
            return HttpResponseRedirect(reverse_lazy("users_app:usergroup_list"))

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        form_invalid_message(self.request)
        return self.render_to_response(ctx)


# RESTRICTIONS


class RestrictionList(generic.ListView):
    # login_url = "/login"
    model = Restrictions
    template_name = "restrictions/restriction_list.html"
    paginate_by = 25

    def get_queryset(self):
        data = Restrictions.objects.all().order_by("id")
        return data

    def get_context_data(self, **kwargs):
        context = super(RestrictionList, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = restriction_title
        context["description_view"] = restriction_desc
        return context


class RestrictionCreate(generic.CreateView):
    # login_url = "/login"
    model = Restrictions
    form_class = RestrictionForm
    template_name = "restrictions/restriction_create_modal.html"

    def get_success_url(self):
        created_message(self.request)
        return reverse_lazy("users_app:restriction_list")

    def get_context_data(self, **kwargs):
        context = super(RestrictionCreate, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = restriction_title
        context["description_view"] = restriction_desc
        return context

    def form_valid(self, form):
        count_code, count_name = diplicate_restrictions(self, form)
        if count_code > 0 or count_name > 0:
            duplicate_message(self.request)
            return HttpResponseRedirect(reverse_lazy("users_app:restriction_list"))
        try:
            return super().form_valid(form)
        except Exception as exception:
            error_message(self.request)
            print(" ")
            print(exception)
            return HttpResponseRedirect(reverse_lazy("users_app:restriction_list"))

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        form_invalid_message(self.request)
        return self.render_to_response(ctx)


class RestrictionEditModal(generic.UpdateView):
    # login_url = '/login'
    model = Restrictions
    form_class = RestrictionForm
    template_name = "restrictions/restriction_update_modal.html"

    def get_success_url(self):
        updated_message(self.request)
        return reverse_lazy("users_app:restriction_list")

    def get_context_data(self, **kwargs):
        context = super(RestrictionEditModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = restriction_title
        context["description_view"] = restriction_desc
        return context

    def form_valid(self, form):
        count_code, count_name = diplicate_restrictions(self, form)
        if count_code > 0 or count_name > 0:
            duplicate_message(self.request)
            return HttpResponseRedirect(reverse_lazy("users_app:restriction_list"))
        try:
            form.instance.updated_at = datetime.now()
            return super().form_valid(form)
        except Exception as exception:
            error_message(self.request)
            print(" ")
            print(exception)
            return HttpResponseRedirect(reverse_lazy("users_app:restriction_list"))

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        form_invalid_message(self.request)
        return self.render_to_response(ctx)


class RestrictionDeleteModal(generic.UpdateView):
    # login_url = '/login'
    model = Restrictions
    form_class = FormDelete
    template_name = "restrictions/restriction_delete_modal.html"

    def get_success_url(self):
        deleted_message(self.request)
        return reverse_lazy("users_app:restriction_list")

    def get_context_data(self, **kwargs):
        context = super(RestrictionDeleteModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = restriction_title
        context["description_view"] = restriction_desc
        return context

    def form_valid(self, form):
        try:
            form.instance.deleted_at = datetime.now()
            return super().form_valid(form)
        except Exception as exception:
            error_message(self.request)
            print(" ")
            print(exception)
            return HttpResponseRedirect(reverse_lazy("users_app:restriction_list"))

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        form_invalid_message(self.request)
        return self.render_to_response(ctx)


# APPS
class AppList(generic.ListView):
    # login_url = "/login"
    model = Apps
    template_name = "apps/app_list.html"
    paginate_by = 25

    def set_urls_in_db(self):
        """
        It takes a list of dictionaries, each dictionary containing a name and route, and saves them to
        the database
        """
        urls = get_url_names()

        for url in urls:
            objects = Apps.objects.all()
            name_count = objects.filter(name__exact=url["name"]).count()
            route_count = objects.filter(route__exact=url["route"]).count()
            if name_count == 0 or route_count == 0:
                app = Apps(
                    name = url["name"],
                    route = url["route"],
                    description = 'App'
                )
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


class AppEditModal(generic.UpdateView):
    # login_url = '/login'
    model = Apps
    form_class = AppForm
    template_name = "apps/app_update_modal.html"

    def get_success_url(self):
        updated_message(self.request)
        return reverse_lazy("users_app:app_list")

    def get_context_data(self, **kwargs):
        context = super(AppEditModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = app_view_title
        context["description_view"] = app_view_desc
        return context

    def form_valid(self, form):
        count_name, count_route = diplicate_apps(self, form)
        if count_name > 0 or count_route > 0:
            duplicate_message(self.request)
            return HttpResponseRedirect(reverse_lazy("users_app:app_list"))
        try:
            form.instance.updated_at = datetime.now()
            return super().form_valid(form)
        except Exception as exception:
            error_message(self.request)
            print(" ")
            print(exception)
            return HttpResponseRedirect(reverse_lazy("users_app:app_list"))

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        form_invalid_message(self.request)
        return self.render_to_response(ctx)
