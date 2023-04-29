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
        offers_cache = (
            Offers.objects.exclude(id=obj.id)
            .filter(
                deleted_at=None,
            )
            .order_by("-created_at", "updated_at")
        )

        offers = offers_cache.filter(Q(tags__in=obj.get_tags()))

        if not offers:
            offers = offers_cache.filter(deleted_at=None)

        offers = offers[:2]

        user = self.request.user

        candidatures = Candidatures.objects.filter(
            offer=obj.id, deleted_at=None
        ).exclude(status="2")

        usergroups = UserRules.objects.filter(
            user=user, usergroup__code__icontains="COM"
        )

        candidature = candidatures.filter(candidate=user)

        context["usergroups"] = usergroups
        context["allowed"] = self.get_object().user == user
        context["similar_offers"] = offers
        context["candidature"] = candidature and candidature.first()
        context["candidatures"] = candidatures
        context["app_title"] = app_title
        context["title_view"] = offer_detail_title
        context["description_view"] = offer_desc
        context["in_offer"] = True
        context["in_offer_detail"] = True
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
        if self.request.user.is_staff:
            return reverse_lazy("offer_app:offer_list")
        return reverse_lazy("offer_app:mypublications")

    def get_context_data(self, **kwargs):
        context = super(OfferDeleteModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = offer_title
        context["description_view"] = offer_desc
        return context

    def form_valid(self, form):
        # offer = self.get_object()
        # validate = Candidatures.objects.filter(offer=offer)
        # if validate:
        #     warning_message(self.request, msg="No se puede ")
        form.instance.deleted_at = timezone.now()
        return super().form_valid(form)


class BiddingPanel(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = Offers
    template_name = "offers/bidding_panel.html"
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get("search", "true")
        return self.model.objects.search(text=search, order="-created_at").filter(
            deleted_at=None
        )

    def get_context_data(self, **kwargs):
        context = super(BiddingPanel, self).get_context_data(**kwargs)
        search = self.request.GET.get("search", "true")
        if not search:
            search = "true"
        context["app_title"] = app_title
        context["title_view"] = offer_title
        context["search"] = search
        context["usergroups"] = UserRules.objects.filter(
            user=self.request.user, usergroup__code__icontains="COM"
        ).count()
        context["in_offer"] = True
        context["search_results"] = self.get_queryset()
        return context


# PUBLICATIONS


class PublicationList(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = Offers
    template_name = "publications/publication_list.html"
    paginate_by = 10

    def get_queryset(self):
        username = self.kwargs.get("username", "")
        objects = (
            self.model.objects.all()
            .filter(user__username=username)
            .annotate(candidatures=Count(F("candidature_offer")))
            .order_by("id")
        )
        pprint(list(objects.values()))

        return objects.exclude(Q(candidatures=0) & ~Q(deleted_at=None))

    def get_context_data(self, **kwargs):
        context = super(PublicationList, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = candidature_title
        context["description_view"] = candidature_desc
        context["in_mypublications"] = True
        return context


class PublicationCreate(LoginRequiredMixin, generic.CreateView):
    login_url = "/login"
    model = Offers
    form_class = OfferForm
    template_name = "publications/publication_create.html"

    def get_success_url(self):
        success_message(self.request)
        return reverse_lazy("offer_app:bidding_panel")

    def get_context_data(self, **kwargs):
        context = super(PublicationCreate, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = offer_create_title
        context["description_view"] = offer_desc
        context["in_mypublications"] = True
        context["in_mypublications_add"] = True
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


class PublicationEdit(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Offers
    form_class = OfferForm
    template_name = "publications/publication_update.html"

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
        context = super(PublicationEdit, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = offer_update_title
        context["description_view"] = offer_desc
        context["in_mypublications"] = True
        context["in_mypublications_edit"] = True
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


class CandidaturesByOfferList(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = Candidatures
    template_name = "candidatures/candidates_by_offer.html"
    paginate_by = 10

    def get_queryset(self):
        str_pk = get_pk_from_a_slug(self)
        return (
            self.model.objects.filter(offer__id=str_pk)
            .exclude(status="2")
            .order_by("created_at")
        )

    def get_context_data(self, **kwargs):
        context = super(CandidaturesByOfferList, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = candidature_title
        context["description_view"] = candidature_desc
        context["mycandidacies"] = True
        return context


class MyCandidacies(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = Candidatures
    template_name = "candidatures/my_candidacies.html"
    paginate_by = 10

    def get_queryset(self):
        username = self.kwargs.get("username", "")
        return self.model.objects.filter(candidate__username=username).order_by(
            "-status", "created_at", "updated_at"
        )

    def get_context_data(self, **kwargs):
        context = super(MyCandidacies, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = candidature_title
        context["description_view"] = candidature_desc
        context["mycandidacies"] = True
        return context


class CandidatureSave(LoginRequiredMixin, generic.FormView):
    login_url = "/login"
    model = Candidatures
    form_class = CandidatureSaveForm
    template_name = "candidatures/candidature_save.html"
    paginate_by = 10

    def get_success_url(self):
        slug = self.kwargs.get("slug", "")
        p_status = self.request.GET.get("status", "")
        p_path = self.request.GET.get("path", "")
        username = self.kwargs.get("username", "")

        status_name = get_status_name(p_status)

        if p_path:
            success_message(
                self.request,
                msg=f"Has {status_name} esta candidatura satisfactoriamente",
            )
            return reverse_lazy(
                f"offer_app:{p_path}", args=[self.request.user.username]
            )

        allowed = self.request.user.is_authenticated

        if not allowed:
            allowed = UserRules.objects.filter(
                user__username=username, usergroup__name="COM"
            )

        if p_status and allowed:
            success_message(
                self.request,
                msg=f"El candidato ha sido {status_name} satisfactoriamente",
            )
            return reverse_lazy("offer_app:candidature_list", args=[slug])

        success_message(self.request, msg="Acción realizada satisfactoriamente")
        return reverse_lazy("offer_app:offer_detail", args=[slug])

    def get_context_data(self, **kwargs):
        p_status = self.request.GET.get("status", "")
        p_path = self.request.GET.get("path", "")
        username = self.kwargs.get("username", "")
        slug = self.kwargs.get("slug", "")

        context = super(CandidatureSave, self).get_context_data(**kwargs)

        str_pk = get_pk_from_a_slug(self)

        context["object"] = Offers.objects.get(pk=str_pk)
        context["slug"] = slug
        context["username"] = username
        context["status"] = p_status
        context["path"] = p_path
        context["app_title"] = app_title
        context["title_view"] = candidature_title
        context["description_view"] = candidature_desc
        return context

    def form_valid(self, form):
        username = self.kwargs.get("username", "")
        p_status = self.request.GET.get("status", "")

        str_pk = get_pk_from_a_slug(self)
        # user = self.request.user
        cantidatures = Candidatures.objects.filter(
            candidate__username=username, offer_id=str_pk
        )

        # if p_status:
        #     status_name = p_status
        # else:
        #     status_name = "postulado"

        # status = POST_STATUS.objects.get(name=status_name)

        if cantidatures:
            cantidature_cache = cantidatures.filter(deleted_at=None)
            if cantidature_cache:
                cantidatures.update(
                    status=p_status, updated_at=timezone.now(), deleted_at=None
                )
        else:
            user = User.objects.get(username=username)
            candidature = Candidatures(offer_id=str_pk, status=p_status, candidate=user)
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
        form.instance.status = "3"
        form.instance.deleted_at = timezone.now()
        return super().form_valid(form)
