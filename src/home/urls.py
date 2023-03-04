# DJANGO MODULES
from django.contrib import admin
from django.urls import path

# PROJECT MODULES
from .views import *

app_name = "home_app"

urlpatterns = [
    path("", HomeView.as_view(), name="home_page"),
    path("help", HelpView.as_view(), name="help"),
    path("profile", ProfileView.as_view(), name="profile"),
    path("profile_company", ProfileCompanyView.as_view(), name="profile_company"),
    path("notifications", NotificationsView.as_view(), name="notifications"),
    path("publicate", PublicateView.as_view(), name="publish"),
    path("oferts", OfertsView.as_view(), name="oferts"),
    path("postulations", PostulationView.as_view(), name="postulate"),
    path("new_publicate", NewPublicateView.as_view(), name="new_publish"),
    
]