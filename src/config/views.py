from django.shortcuts import render
from django.views import generic
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from core.utils import get_request_body, set_data_status
from .models import *
from pprint import pprint

app_title = _("Config")
contact_title = _("Soporte")
contact_description = _("Póngase en contacto con nuestro equipo de atención al cliente")
contact_exception = _(
    "Si no puede comunicarse por estos medios, hágalo desde nuestras redes sociales"
)


# Create your views here.
class ContactList(generic.ListView):
    model = Contact
    template_name = "contact/contact.html"

    def get_queryset(self):
        return Contact.objects.all().order_by("id")

    def get_context_data(self, **kwargs):
        context = super(ContactList, self).get_context_data(**kwargs)
        context["app_title"] = contact_title
        context["title_view"] = contact_title
        context["description_view"] = contact_description
        context["exception_view"] = contact_exception
        context["social_networks"] = SocialNetwork.objects.all()

        try:
            context["defaultContact"] = Contact.objects.get(
                city__name__icontains="BUCARAMANGA"
            )
        except:
            pass

        context[
            "image_url"
        ] = "core/assets/img/annie-spratt-goholCAVTRs-unsplash-compressed.jpg"
        context["image_alt"] = "annie-spratt-goholCAVTRs-unsplash"
        return context


class APIContact(generic.View):
    def post(self, request, *args, **kwargs):
        body = get_request_body(request)
        city = body["city"]
        try:
            contact = Contact.objects.filter(city__name__icontains=city).values()[0]
            data = set_data_status(data=contact)
        except Exception as ex:
            print(f"Error in APIContact ~ POST: {ex}")
            data = set_data_status()
        return JsonResponse(data, safe=False)
