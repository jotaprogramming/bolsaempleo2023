# DJANGO MODULES
from django.contrib import admin
from django.urls import path

# PROJECT MODULES
from .views import *

app_name = "home_app"

urlpatterns = [
    path("", HomeView.as_view(), name="home_page"),
    path("help", HelpView.as_view(), name="help"),
    
]