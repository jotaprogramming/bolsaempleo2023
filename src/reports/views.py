from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.views import generic
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

from offers.models import Offers
from users.models import UserGroups

# GLOBAL VARIABLES
app_title = _("Reportes")
reports_page_title = _("Panel de reportes")
reports_page_desc = _("Reportes de usuarios y ofertas")
user_report_title = _("Usuarios")
user_report_desc = _("Panel de reportes de los usuarios 'empresa' y 'egresado'")
offer_report_title = _("Ofertas")
offer_report_desc = _("Listado de las ofertas publicadas")


# Create your views here.
class ReportsHome(LoginRequiredMixin, generic.TemplateView):
    login_url = "/login"
    template_name = "reports/reports_home.html"

    def get_context_data(self, **kwargs):
        context = super(ReportsHome, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = reports_page_title
        context["description_view"] = reports_page_desc
        context["reports"] = True
        return context


class UserReport(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = User
    template_name = "reports/user_report.html"
    paginate_by = 10

    def get_queryset(self):
        usergroup = self.request.GET.get("usergroup", "")
        obj = self.model.objects.all().order_by("id")
        if usergroup:
            obj = obj.filter(rule_user__usergroup__code__in=[usergroup])
        return obj

    def get_context_data(self, **kwargs):
        context = super(UserReport, self).get_context_data(**kwargs)
        usergroup = self.request.GET.get("usergroup", "")

        title_view = user_report_title
        description_view = user_report_desc

        if usergroup:
            usergroup_obj = UserGroups.objects.get(code=usergroup)
            title_view = usergroup_obj.group_name
            description_view = f"Listado de los usuarios '{title_view}'"

        context["app_title"] = app_title
        context["title_view"] = title_view.capitalize()
        context["description_view"] = description_view
        context["reports"] = True
        return context


class OfferReport(LoginRequiredMixin, generic.ListView):
    login_url = "/login"
    model = Offers
    template_name = "reports/offer_report.html"
    paginate_by = 10

    def get_queryset(self):
        tag = self.request.GET.get("tag", "")
        order = self.request.GET.get("order", "-created_at")

        obj = self.model.objects.all()
        if "count" in order:
            obj = obj.annotate(count=Count(F("candidature_offer")))
        if "ctags" in order:
            obj = obj.annotate(ctags=Count(F("tags")))
        if tag:
            obj = obj.filter(tags__name__in=[tag])
        return obj.order_by(order)

    def get_context_data(self, **kwargs):
        context = super(OfferReport, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = offer_report_title
        context["description_view"] = offer_report_desc
        context["reports"] = True
        return context
