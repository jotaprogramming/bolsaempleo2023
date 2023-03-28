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
from django.core import signing

# EXTRA MODULES
import sweetify

# PROJECT MODULES
from offers.forms import *
from offers.models import *
from core.utils import *
from users.models import *
from users.forms import FormDelete
from jobboard.utils import *


# GLOBAL VARIABLES
app_title = _("Ofertas")
offer_title = _("Ofertas")
offer_desc = _("Ofertas")
offer_create_title = _("Publicar")
offer_update_title = _("Editar")
offer_detail_title = _("Detalle")
candidature_title = _("Postulaciones")
candidature_desc = _("Postulaciones")


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
        return reverse_lazy("offer_app:bidding_panel")

    def get_context_data(self, **kwargs):
        context = super(OfferCreate, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = offer_create_title
        context["description_view"] = offer_desc
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


class OfferEdit(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Offers
    form_class = OfferForm
    template_name = "offers/offer_update.html"

    slug = ""

    def get_object(self):
        self.slug = self.kwargs.get("slug", "")
        slug_split = self.slug.split("-")
        split_pk = slug_split[-1]
        # str_pk = base64_to_string(f"{split_pk}")
        str_pk = split_pk

        return self.model.objects.get(pk=str_pk)

    def get_success_url(self):
        success_message(self.request, msg="Oferta actualizada satisfactoriamente")
        return reverse_lazy("offer_app:offer_detail", args=[self.slug])

    def get_context_data(self, **kwargs):
        self.slug = self.kwargs.get("slug", "")
        context = super(OfferEdit, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = offer_update_title
        context["description_view"] = offer_desc
        return context

    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        form.instance.user = self.request.user
        form.instance.title = str(form.instance.title).upper()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(
            reverse_lazy("offer_app:offer_edit", args=[self.slug])
        )


class OfferDetail(LoginRequiredMixin, generic.DetailView):
    login_url = "/login"
    model = Offers
    template_name = "offers/offer_detail.html"

    def get_object(self):
        str_pk = get_pk_from_a_slug(self)

        return self.model.objects.get(pk=str_pk)

    def get_context_data(self, **kwargs):
        context = super(OfferDetail, self).get_context_data(**kwargs)
        obj = self.get_object()
        offers = (
            Offers.objects.exclude(id=obj.id)
            .filter(
                Q(tags__in=obj.get_tags()),
                deleted_at=None,
            )
            .order_by("-created_at")[:2]
        )

        user = self.request.user
        if not self.request.user.is_staff:
            usergroups = Traits.objects.filter(
                user=user, usergroup__code__icontains="COM"
            )
            context["usergroups"] = usergroups

        context["offer"] = True
        context["similar_offers"] = offers
        context["candidature"] = Candidatures.objects.filter(
            candidate=user, offer=obj.id, deleted_at=None
        )
        context["app_title"] = app_title
        context["title_view"] = offer_detail_title
        context["description_view"] = offer_desc
        return context


class OfferModalCreate(LoginRequiredMixin, generic.CreateView):
    login_url = "/login"
    model = Offers
    form_class = OfferAdminForm
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
    form_class = OfferAdminForm
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


class BiddingPanel(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = Offers
    template_name = "offers/bidding_panel.html"
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get("search", "true")
        return Offers.objects.search(text=search, order="-created_at")

    def get_context_data(self, **kwargs):
        context = super(BiddingPanel, self).get_context_data(**kwargs)
        search = self.request.GET.get("search", "true")
        if not search:
            search = "true"
        context["app_title"] = app_title
        context["title_view"] = offer_title
        context["search"] = search
        return context


# CANDIDATURES
class CandidaturesList(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = Candidatures
    template_name = "candidatures/candidature_list.html"
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.all().order_by("id")

    def get_context_data(self, **kwargs):
        context = super(CandidaturesList, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = candidature_title
        context["description_view"] = candidature_desc
        return context


class CandidatureSave(LoginRequiredMixin, generic.FormView):
    login_url = "/login"
    model = Candidatures
    form_class = CandidatureSaveForm
    template_name = "candidatures/candidature_save.html"
    paginate_by = 10

    def get_success_url(self):
        slug = self.kwargs.get("slug", "")
        success_message(self.request, msg="Postulación realizada satisfactoriamente")
        return reverse_lazy("offer_app:offer_detail", args=[slug])

    def get_context_data(self, **kwargs):
        context = super(CandidatureSave, self).get_context_data(**kwargs)

        str_pk = get_pk_from_a_slug(self)

        try:
            context["object"] = Offers.objects.get(pk=str_pk)
        except Exception as e:
            print(
                f"An exception occurred in <<get_context_data>> of <<CandidatureSave>>: {e}"
            )

        context["app_title"] = app_title
        context["title_view"] = candidature_title
        context["description_view"] = candidature_desc
        return context

    def form_valid(self, form):
        str_pk = get_pk_from_a_slug(self)
        user = self.request.user
        cantidatures = Candidatures.objects.filter(candidate=user, offer_id=str_pk)
        status = PostStatus.objects.get(name="postulado")
        if cantidatures:
            cantidature_cache = cantidatures.exclude(deleted_at=None)
            if cantidature_cache:
                cantidatures.update(
                    status=status, updated_at=timezone.now(), deleted_at=None
                )
        else:
            candidature = Candidatures(offer_id=str_pk, status=status, candidate=user)
            candidature.save()

        return super().form_valid(form)


class CandidatureEditModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Candidatures
    form_class = CandidatureUpdateForm
    template_name = "candidatures/candidature_update_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Postulación actualizada satisfactoriamente")
        return reverse_lazy("offer_app:candidature_list")

    def get_context_data(self, **kwargs):
        context = super(CandidatureEditModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = candidature_title
        context["description_view"] = candidature_desc
        return context

    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("offer_app:candidature_list"))


class CandidatureDeleteModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Candidatures
    form_class = FormDelete
    template_name = "candidatures/candidature_delete_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Postulación eliminada satisfactoriamente")
        return reverse_lazy("offer_app:candidature_list")

    def get_context_data(self, **kwargs):
        context = super(CandidatureDeleteModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = candidature_title
        context["description_view"] = candidature_desc
        return context

    def form_valid(self, form):
        form.instance.status = PostStatus.objects.get(name="rechazado")
        form.instance.deleted_at = timezone.now()
        return super().form_valid(form)
