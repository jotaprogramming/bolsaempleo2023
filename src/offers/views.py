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
from offers.forms import *
from offers.models import *
from offers.utils import *
from core.utils import *
from users.forms import FormDelete
from jobboard.utils import *


# GLOBAL VARIABLES
app_title = _("Ofertas")
offer_title = _("Ofertas")
offer_desc = _("Ofertas")
offer_detail_title = _("Detalle")


# OFFERS
class OfferList(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = Offers
    template_name = "offers/offer_list.html"
    paginate_by = 10

    def get_queryset(self):
        return Offers.objects.all().order_by("id")

    def get_context_data(self, **kwargs):
        context = super(OfferList, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = offer_title
        context["description_view"] = offer_desc
        return context


class OfferCreate(LoginRequiredMixin, generic.CreateView):
    login_url = "/login"
    model = Offers
    form_class = OfferForm
    template_name = "offers/offer_create.html"

    def get_success_url(self):
        success_message(self.request)
        return reverse_lazy("offer_app:offer_list")

    def get_context_data(self, **kwargs):
        context = super(OfferCreate, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.title = str(form.instance.title).upper()
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return self.render_to_response(ctx)


class OfferDetail(LoginRequiredMixin, generic.DetailView):
    login_url = "/login"
    model = Offers
    template_name = "offers/offer_detail.html"

    def get_context_data(self, **kwargs):
        context = super(OfferDetail, self).get_context_data(**kwargs)
        obj = self.get_object()
        offers = Offers.objects.exclude(id=obj.id).filter(
            Q(tags__in=obj.get_tags()),
            deleted_at=None,
        ).order_by("-created_at")[:2]
        pprint(offers)
        context["offer"] = True
        context["offers"] = offers
        context["app_title"] = app_title
        context["title_view"] = offer_detail_title
        context["description_view"] = offer_desc
        return context


class OfferModalCreate(LoginRequiredMixin, generic.CreateView):
    login_url = "/login"
    model = Offers
    form_class = OfferForm
    template_name = "offers/offer_create_modal.html"

    def get_success_url(self):
        success_message(self.request)
        return reverse_lazy("offer_app:offer_list")

    def get_context_data(self, **kwargs):
        context = super(OfferModalCreate, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.title = str(form.instance.title).upper()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("offer_app:offer_list"))


class OfferEditModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Offers
    form_class = OfferForm
    template_name = "offers/offer_update_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Oferta actualizada satisfactoriamente")
        return reverse_lazy("offer_app:offer_list")

    def get_context_data(self, **kwargs):
        context = super(OfferEditModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = offer_title
        context["description_view"] = offer_desc
        return context

    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        form.instance.title = str(form.instance.title).upper()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("offer_app:offer_list"))


class OfferDeleteModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Offers
    form_class = FormDelete
    template_name = "Offers/offer_delete_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Oferta eliminada satisfactoriamente")
        return reverse_lazy("offer_app:offer_list")

    def get_context_data(self, **kwargs):
        context = super(OfferDeleteModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = offer_title
        context["description_view"] = offer_desc
        return context

    def form_valid(self, form):
        form.instance.deleted_at = timezone.now()
        return super().form_valid(form)