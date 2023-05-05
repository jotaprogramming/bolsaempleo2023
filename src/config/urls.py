# DJANGO MODULES
from django.contrib import admin
from django.urls import path

# PROJECT MODULES
from .views import *

app_name = "config_app"

urlpatterns = [
    path("contact", ContactList.as_view(), name="contact"),
    path("api/get/contact", APIContact.as_view(), name="get_contact"),
]
