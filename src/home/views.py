# DJANGO MODULES
from django.shortcuts import render
from django.views import generic
from django.utils.translation import gettext_lazy as _

# GLOBAL VARIABLES
app_title = _("Home")
home_title = _("Bolsa de Empleo")
home_desc = _("Proyecto de grado 2023")
help_title = _("Ayuda")
help_desc = _("Contacto")
profile_title = _("Profile")
profile_view = _("Perfil")
profilecompany_title = _("CompanyProfile")
profilecompany_view = _("Perfil Empresarial")
notifications_title = _("Notifications")
notifications_view = _("Notificaciones")
ofert_title = _("Ofertas")
ofert_view = _("Ofertas")
new_publish = _("Crear Nuevo")
publish_view = _("Publicar")
postulate_view = _("Postular")


class HomeView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["app_title"] = app_title
        context["title_view"] = home_title
        context["description_view"] = home_desc
        return context
    
    
class HelpView(generic.TemplateView):
    help_url = '/help'
    template_name='help.html'
    
    def get_context_data(self, **kwargs):
        context = super(HelpView, self).get_context_data(**kwargs)
        context["app_title"] = help_title
        context["title_view"] = help_desc
        #context["img_url"] = 'static/core/assets/img/login.jpg'
        return context
    
    
class ProfileView(generic.TemplateView):
    profile_url = '/profile'
    template_name='profile.html'
    
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context["app_title"] = profile_title
        context["title_view"] = profile_view
        return context


class ProfileCompanyView(generic.TemplateView):
    profile_url = '/profile_company'
    template_name='profile_company.html'
    
    def get_context_data(self, **kwargs):
        context = super(ProfileCompanyView, self).get_context_data(**kwargs)
        context["app_title"] = profilecompany_title
        context["title_view"] = profilecompany_view
        return context
    
    
class NotificationsView(generic.TemplateView):
    profile_url = '/notifications'
    template_name='notifications.html'
    
    def get_context_data(self, **kwargs):
        context = super(NotificationsView, self).get_context_data(**kwargs)
        context["app_title"] = notifications_title
        context["title_view"] = notifications_view
        return context
    
    
    
    
class PublicateView(generic.TemplateView):
    profile_url = '/publicate'
    template_name='publish.html'
    
    def get_context_data(self, **kwargs):
        context = super(PublicateView, self).get_context_data(**kwargs)
        context["app_title"] = ofert_view
        context["title_view"] = publish_view
        return context
    
    

class OfertsView(generic.TemplateView):
    profile_url = '/oferts'
    template_name='oferts.html'
    
    def get_context_data(self, **kwargs):
        context = super(OfertsView, self).get_context_data(**kwargs)
        context["app_title"] = ofert_title
        context["title_view"] = ofert_view
        return context
    
    

class PostulationView(generic.TemplateView):
    profile_url = '/postulations'
    template_name='postulations.html'
    
    def get_context_data(self, **kwargs):
        context = super(PostulationView, self).get_context_data(**kwargs)
        context["app_title"] = ofert_title
        context["title_view"] = postulate_view
        return context
    
    
    
class NewPublicateView(generic.TemplateView):
    profile_url = '/new_publicate'
    template_name='new_publish.html'
    
    def get_context_data(self, **kwargs):
        context = super(NewPublicateView, self).get_context_data(**kwargs)
        context["app_title"] = ofert_title
        context["title_view"] = new_publish
        return context