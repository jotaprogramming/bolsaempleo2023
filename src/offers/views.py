# PYTHON MODULES
from datetime import datetime
import json

# DJANGO MODULES
from django.contrib.auth.models import User
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
from django.db.models import Q, F, Count, Sum, Case, When, BooleanField, IntegerField
from django.utils import timezone

# EXTRA MODULES
import sweetify
from notifications.signals import notify
from notifications.models import Notification

# PROJECT MODULES
from offers.forms import (
    OfferAdminForm,
    OfferForm,
    CandidatureSaveForm,
    CandidatureUpdateForm,
)
from offers.models import Tags, Offers, Candidatures
from offers.utils import (
    get_pk_from_a_slug,
    send_new_offer_notification,
    get_status_name,
    send_notification_of_candidacy_status,
    OFFER_STATUS,
    POST_STATUS,
)
from core.utils import success_message, warning_message, get_form_errors
from users.models import UserRules
from users.forms import FormDelete
from jobboard.utils import *

# GLOBAL VARIABLES
app_title = _("Ofertas")
offer_title = _("Ofertas")
offer_desc = _("Ofertas")
offer_create_title = _("Publicar")
offer_update_title = _("Editar")
offer_detail_title = _("Detalle")
publication_title = _("Publicaciones")
publication_desc = _("Listado de mis publicaciones")
candidature_title = _("Candidaturas")
candidature_desc = _("Postulaciones a ofertas laborales")
candidature_offer_title = _("Candidaturas")
candidature_offer_desc = _("Postulaciones de la oferta")


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
        offer = self.get_object()
        offers_cache = (
            Offers.objects.exclude(id=offer.id)
            .filter(
                deleted_at=None,
            )
            .order_by("-created_at", "updated_at")
        )

        offers = offers_cache.filter(Q(tags__in=offer.get_tags()))

        if not offers:
            offers = offers_cache.filter(deleted_at=None)

        offers = offers[:2]

        user = self.request.user

        candidatures = Candidatures.objects.filter(
            offer=offer.id, deleted_at=None
        )

        allowed_to_apply = UserRules.objects.filter(user=user, usergroup__code="GRA")
        allowed_to_edit = UserRules.objects.filter(
            user=user,
            user__offer_user=offer.id,
            usergroup__usergroup_policy__app__name="offers_app:offer_edit",
        )
        allowed_to_candidates = UserRules.objects.filter(
            Q(
                user=user,
                usergroup__code="MOD",
                usergroup__usergroup_policy__app__name="offers_app:candidature_list",
            )
            | Q(user=user, usergroup__code="COM", user__offer_user=offer.id),
        )
        # company = UserRules.objects.filter(user__offer_user=self.get_object(), usergroup__code__icontains="COM")

        candidature = candidatures.filter(candidate=user)

        context["allowed_to_apply"] = allowed_to_apply
        context["allowed_to_edit"] = allowed_to_edit
        context["allowed_to_candidates"] = allowed_to_candidates
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
        return reverse_lazy("offers_app:offer_list")

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
        return HttpResponseRedirect(reverse_lazy("offers_app:offer_list"))


class OfferEditModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Offers
    form_class = OfferAdminForm
    template_name = "offers/offer_update_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Oferta actualizada satisfactoriamente")
        return reverse_lazy("offers_app:offer_list")

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
        return HttpResponseRedirect(reverse_lazy("offers_app:offer_list"))


class OfferDeleteModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Offers
    form_class = FormDelete
    template_name = "Offers/offer_delete_modal.html"

    def get_object(self):
        pk = get_pk_from_a_slug(self)
        return self.model.objects.get(pk=pk)

    def get_success_url(self):
        success_message(self.request, msg="Oferta eliminada satisfactoriamente")
        offer = self.get_object()
        Candidatures.objects.filter(offer=offer, status="1").update(
            status="2", updated_at=timezone.now()
        )
        if self.request.user.is_staff:
            return reverse_lazy("offers_app:offer_list")
        return reverse_lazy(
            "offers_app:mypublications", args=[self.request.user.username]
        )

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


class OfferFinishModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Offers
    form_class = FormDelete
    template_name = "Offers/offer_finish_modal.html"

    def get_object(self):
        pk = get_pk_from_a_slug(self)
        return self.model.objects.get(pk=pk)

    def get_success_url(self):
        success_message(self.request, msg="Oferta finalizada satisfactoriamente")
        offer = self.get_object()
        Candidatures.objects.filter(offer=offer, status="1").update(
            status="2", updated_at=timezone.now()
        )
        # if self.request.user.is_staff:
        #     return reverse_lazy("offers_app:offer_list")
        return reverse_lazy(
            "offers_app:mypublications", args=[self.request.user.username]
        )

    def get_context_data(self, **kwargs):
        context = super(OfferFinishModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = offer_title
        context["description_view"] = offer_desc
        return context

    def form_valid(self, form):
        p_status = self.request.GET.get("status", False)
        if not p_status == "true":
            warning_message(self.request, msg="Esta acción no ha podido completarse")
            return HttpResponseRedirect(
                reverse_lazy(
                    "offers_app:mypublications", args=[self.request.user.username]
                )
            )
        form.instance.status = True
        form.instance.updated_at = timezone.now()
        return super().form_valid(form)


class BiddingPanel(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = Offers
    template_name = "offers/bidding_panel.html"
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get("search", "true")
        order = self.request.GET.get("order", "-created_at")
        return self.model.objects.search(text=search, order=order).filter(
            deleted_at=None, status=False
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
        p_status = self.request.GET.get("status", "")
        p_search = self.request.GET.get("search", "")

        objects = (
            self.model.objects.all()
            .filter(user__username=username)
            .filter(Q(title__icontains=p_search) | Q(title__icontains=p_search))
            .annotate(
                active_candidates=Count(
                    F("candidature_offer"),
                    filter=Q(candidature_offer__status__in=["1", "4"]),
                ),
                cancelled_candidates=Count(
                    F("candidature_offer"),
                    filter=Q(candidature_offer__status__in=["2"]),
                ),
                rejected_candidates=Count(
                    F("candidature_offer"),
                    filter=Q(candidature_offer__status__in=["3"]),
                ),
                accepted_candidates=Count(
                    F("candidature_offer"),
                    filter=Q(candidature_offer__status__in=["4"]),
                ),
                completed_candidates=Count(
                    F("candidature_offer"),
                    filter=Q(candidature_offer__status__in=["5"]),
                ),
            )
            .order_by("-deleted_at", "title")
        )
        if p_status:
            if "!" in p_status:
                status = p_status.replace("!", "")
                validate = status in [item[0] for item in OFFER_STATUS]
                if status == "3" or validate:
                    if status == "1":
                        objects = objects.exclude(deleted_at=None).exclude(status=False)
                    elif status == "2":
                        objects = objects.filter(deleted_at=None).exclude(status=True)
                    else:
                        objects = objects.filter(deleted_at=None)
            else:
                validate = p_status in [item[0] for item in OFFER_STATUS]
                if p_status == "3" or validate:
                    if p_status == "1":
                        objects = objects.filter(deleted_at=None).filter(status=False)
                    elif p_status == "2":
                        objects = objects.filter(deleted_at=None).filter(status=True)
                    else:
                        objects = objects.exclude(deleted_at=None)
        return objects

    def get_context_data(self, **kwargs):
        p_search = self.request.GET.get("search", "")
        p_status = self.request.GET.get("status", "")

        context = super(PublicationList, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = publication_title
        context["description_view"] = publication_desc
        context["in_mypublications"] = True
        context["search"] = p_search
        context["pstatus"] = p_status
        # statuses = POST_STATUS[:1] + POST_STATUS[2:]
        context["statuses"] = (
            ("1", "activa"),
            ("2", "finalizada"),
            ("3", "eliminada"),
        )
        return context


class PublicationCreate(LoginRequiredMixin, generic.CreateView):
    login_url = "/login"
    model = Offers
    form_class = OfferForm
    template_name = "publications/publication_create.html"

    tags = []

    def get_success_url(self):
        self.object.tags.set(self.tags)

        send_new_offer_notification(self)
        success_message(self.request)
        return reverse_lazy("offers_app:bidding_panel")

    def get_context_data(self, **kwargs):
        context = super(PublicationCreate, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = offer_create_title
        context["description_view"] = offer_desc
        context["in_mypublications"] = True
        context["in_mypublications_add"] = True
        context["tag_datalist"] = Tags.objects.all()
        return context

    def form_valid(self, form):
        form_tags = form.cleaned_data["tags"]
        tag_list = form_tags.split(",")

        self.tags = []
        for tag in tag_list:
            try:
                objtag = Tags.objects.get(name__icontains=tag)
                self.tags.append(objtag)
            except:
                pass

        # form.cleaned_data["tags"] = temp_list
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
        return reverse_lazy("offers_app:offer_detail", args=[self.slug])

    def get_context_data(self, **kwargs):
        self.slug = self.kwargs.get("slug", "")
        context = super(PublicationEdit, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = offer_update_title
        context["description_view"] = offer_desc
        context["in_mypublications"] = True
        context["in_mypublications_edit"] = True
        context["tag_datalist"] = Tags.objects.all()
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
            reverse_lazy("offers_app:offer_edit", args=[self.slug])
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
        p_status = self.request.GET.get("status", "")
        p_search = self.request.GET.get("search", "")
        # status_name = get_status_name(p_status)

        str_pk = get_pk_from_a_slug(self)
        obj = (
            self.model.objects.filter(offer__id=str_pk).filter(
                Q(candidate__first_name__icontains=p_search)
                | Q(candidate__last_name__icontains=p_search)
            )
            # .exclude(status__in=["2"])
            .order_by("-updated_at")
        )

        if p_status:
            if "!" in p_status:
                status = p_status.replace("!", "")
                obj = obj.exclude(status=status)
            else:
                obj = obj.filter(status=p_status)

        return obj

    def get_context_data(self, **kwargs):
        p_status = self.request.GET.get("status", "")
        p_search = self.request.GET.get("search", "")
        str_pk = get_pk_from_a_slug(self)
        context = super(CandidaturesByOfferList, self).get_context_data(**kwargs)

        objects = self.get_queryset()
        count = objects.count()

        context["app_title"] = app_title
        context["title_view"] = (
            objects.first().offer.title.capitalize()
            if count
            else Offers.objects.filter(id=str_pk).first().title.capitalize()
        )
        if count == 1:
            desc = "Un candidato ha aplicado a esta oferta"
        elif count > 0:
            desc = f"{count} candidatos han aplicado a esta oferta"
        else:
            desc = "Sin candidatos"
        context["description_view"] = desc
        context["mycandidacies"] = True
        context["statuses"] = POST_STATUS
        context["pstatus"] = p_status
        context["search"] = p_search

        # offer_id = objects.first().offer.id
        # context["rejected_candidates"] = (
        #     self.model.objects.filter(offer__id=offer_id)
        #     .filter(status__in=["2", "3"])
        #     .order_by("updated_at")
        # )
        return context


class MyCandidacies(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = Candidatures
    template_name = "candidatures/my_candidacies.html"
    paginate_by = 10

    def get_queryset(self):
        username = self.kwargs.get("username", "")
        p_status = self.request.GET.get("status", "")
        p_search = self.request.GET.get("search", "")

        obj = (
            self.model.objects.filter(candidate__username=username)
            .filter(
                Q(offer__title__icontains=p_search)
                | Q(offer__title__icontains=p_search)
            )
            .order_by("-offer__deleted_at", "status")
        )
        if p_status:
            if "!" in p_status:
                status = p_status.replace("!", "")
                obj = obj.exclude(status=status)
            else:
                obj = obj.filter(status=p_status)
        return obj

    def get_context_data(self, **kwargs):
        p_status = self.request.GET.get("status", "")
        p_search = self.request.GET.get("search", "")

        context = super(MyCandidacies, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = candidature_title
        context["description_view"] = candidature_desc
        context["mycandidacies"] = True
        context["statuses"] = POST_STATUS
        context["pstatus"] = p_status
        context["search"] = p_search
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
        send_notification_of_candidacy_status(self)

        if p_path:
            success_message(
                self.request,
                msg=f"Has {status_name} esta candidatura satisfactoriamente",
            )
            return reverse_lazy(
                f"offers_app:{p_path}", args=[self.request.user.username]
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
            return reverse_lazy("offers_app:candidature_list", args=[slug])

        success_message(self.request, msg="Acción realizada satisfactoriamente")
        return reverse_lazy("offers_app:offer_detail", args=[slug])

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
        context["title_view"] = publication_title
        context["description_view"] = publication_desc
        return context

    def form_valid(self, form):
        slug = self.kwargs.get("slug", "")
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
            if not cantidature_cache:
                return HttpResponseRedirect(
                    reverse_lazy("offers_app:offer_detail", args=[slug])
                )
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
        return reverse_lazy("offers_app:candidature_list")

    def get_context_data(self, **kwargs):
        context = super(CandidatureEditModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = publication_title
        context["description_view"] = publication_desc
        return context

    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form

        msg_error = get_form_errors(form)
        warning_message(self.request, msg=msg_error)
        return HttpResponseRedirect(reverse_lazy("offers_app:candidature_list"))


class CandidatureDeleteModal(LoginRequiredMixin, generic.UpdateView):
    login_url = "/login"
    model = Candidatures
    form_class = FormDelete
    template_name = "candidatures/candidature_delete_modal.html"

    def get_success_url(self):
        success_message(self.request, msg="Postulación eliminada satisfactoriamente")
        return reverse_lazy("offers_app:candidature_list")

    def get_context_data(self, **kwargs):
        context = super(CandidatureDeleteModal, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = publication_title
        context["description_view"] = publication_desc
        return context

    def form_valid(self, form):
        form.instance.status = "3"
        form.instance.deleted_at = timezone.now()
        return super().form_valid(form)
