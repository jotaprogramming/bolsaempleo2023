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

# EXTRA MODULES
import sweetify

# PROJECT MODULES
from users.forms import *
from users.models import *
from core.utils import *

# PROJECT FORMS

# GLOBAL VARIABLES
title_app = "Grupo de usuarios"


# Create your views here.
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
        context["title_app"] = title_app
        return context


class UserGroupCreate(generic.CreateView):
    # login_url = "/login"
    model = UserGroups
    form_class = UserGroupForm
    template_name = "usergroups/usergroup_create_modal.html"

    def get_success_url(self):
        swal_title = "Éxito"
        swal_msg = "Registro creado satisfactoriamente"
        swal_time = 5000
        sweetify.success(
            self.request,
            title=swal_title,
            text=swal_msg,
            icon="success",
            timer=swal_time,
            timerProgressBar="true",
            button="Ok",
        )
        return reverse_lazy("users_app:usergroup_list")

    def get_context_data(self, **kwargs):
        context = super(UserGroupCreate, self).get_context_data(**kwargs)
        context["title_app"] = title_app
        return context

    def form_valid(self, form):
        group_name = form.instance.group_name
        groups = UserGroups.objects.filter(group_name__exact=group_name).count()
        if groups:
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

        swal_title = "Advertencia"
        swal_msg = "Formulario inválido"
        swal_time = 5000
        sweetify.warning(
            self.request,
            title=swal_title,
            text=swal_msg,
            icon="warning",
            timer=swal_time,
            timerProgressBar="true",
            button="Ok",
        )
        return self.render_to_response(ctx)


class UserGroupEditModal(generic.UpdateView):
    # login_url = '/login'
    model = UserGroups
    form_class = UserGroupForm
    template_name = "usergroups/usergroup_update_modal.html"

    def get_success_url(self):
        swal_title = "Éxito"
        swal_msg = "Registro actualizado satisfactoriamente"
        swal_time = 5000
        sweetify.success(
            self.request,
            title=swal_title,
            text=swal_msg,
            icon="success",
            timer=swal_time,
            timerProgressBar="true",
            button="Ok",
        )
        return reverse_lazy("users_app:usergroup_list")

    def get_context_data(self, **kwargs):
        context = super(UserGroupEditModal, self).get_context_data(**kwargs)
        context["title_app"] = title_app
        return context

    def form_valid(self, form):
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

        swal_title = "Advertencia"
        swal_msg = "Formulario inválido"
        swal_time = 5000
        sweetify.warning(
            self.request,
            title=swal_title,
            text=swal_msg,
            icon="warning",
            timer=swal_time,
            timerProgressBar="true",
            button="Ok",
        )
        return self.render_to_response(ctx)


class UserGroupDeleteModal(generic.UpdateView):
    # login_url = '/login'
    model = UserGroups
    form_class = UserGroupFormDelete
    template_name = "usergroups/usergroup_delete_modal.html"

    def get_success_url(self):
        swal_title = "Éxito"
        swal_msg = "Registro eliminado satisfactoriamente"
        swal_time = 5000
        sweetify.success(
            self.request,
            title=swal_title,
            text=swal_msg,
            icon="success",
            timer=swal_time,
            timerProgressBar="true",
            button="Ok",
        )
        return reverse_lazy("users_app:usergroup_list")

    def get_context_data(self, **kwargs):
        context = super(UserGroupDeleteModal, self).get_context_data(**kwargs)
        context["title_app"] = title_app
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

        swal_title = "Advertencia"
        swal_msg = "Formulario inválido"
        swal_time = 5000
        sweetify.warning(
            self.request,
            title=swal_title,
            text=swal_msg,
            icon="warning",
            timer=swal_time,
            timerProgressBar="true",
            button="Ok",
        )
        return self.render_to_response(ctx)


"""
class HomePage(LoginRequiredMixin, generic.FormView):
    login_url = '/login'
    model = HomePage 
    form_class = HomePageForm
    template_name='home/home_page.html'

    def get_success_url(self):
        messages.success(self.request, '...')
        return reverse_lazy('home_app:home_page')

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)      
        return context 

    def get_queryset(self):
        data = Model.objects.all()
        return data

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)
"""
