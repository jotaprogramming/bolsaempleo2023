# DJANGO MODULES
from django.shortcuts import render
from django.views import generic
from django.utils.translation import gettext_lazy as _

# GLOBAL VARIABLES
app_title = _("Home")
home_title = _("Bolsa de Empleo")
home_desc = _("Proyecto de grado 2023")
help_title = _("ayuda")
help_desc = _("Contacto")


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
    