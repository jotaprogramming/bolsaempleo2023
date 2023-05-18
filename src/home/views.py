# DJANGO MODULES
from django.shortcuts import render
from django.views import generic
from django.utils.translation import gettext_lazy as _

from config.models import SocialNetwork

# GLOBAL VARIABLES
app_title = _("Home")
home_title = _("Bolsa de Empleo")
home_desc = _("Proyecto de grado 2023")
help_title = _("Ayuda")
help_desc = _("Contacto")
profile_title = _("Profile")
profile_view = _("Perfil")
profile_edit = _("Editar")
profilecompany_title = _("CompanyProfile")
profilecompany_view = _("Perfil Empresarial")
notifications_title = _("Notifications")
notifications_view = _("Notificaciones")
offer_title = _("Ofertas")
offer_view = _("Ofertas")
offer_desc = _("Detalles")
new_publish = _("Crear Nuevo")
publish_view = _("Publicar")
postulate_view = _("Postular")
candidate_desc = _("Candidatos")
mod_view = _("Moderate")
mod_desc = _("Moderador")


class HomeView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = home_title
        context["description_view"] = home_desc
        context["social_networks"] = SocialNetwork.objects.all()
        return context


class HelpView(generic.TemplateView):
    help_url = "/help"
    template_name = "help.html"

    def get_context_data(self, **kwargs):
        context = super(HelpView, self).get_context_data(**kwargs)
        context["app_title"] = help_title
        context["title_view"] = help_desc
        context[
            "image_url"
        ] = "core/assets/img/annie-spratt-goholCAVTRs-unsplash-compressed.jpg"
        context["image_alt"] = "annie-spratt-goholCAVTRs-unsplash"
        return context
