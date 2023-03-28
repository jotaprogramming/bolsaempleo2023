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
    path("profile_student", ProfileStudentView.as_view(), name="profile_student"),
    path("notifications", NotificationsView.as_view(), name="notifications"),
    path("publicate", PublicateView.as_view(), name="publish"),
    path("offers", OffersView.as_view(), name="offers"),
    path("postulations", PostulationView.as_view(), name="postulate"),
    path("new_publicate", NewPublicateView.as_view(), name="new_publish"),
    path("edit_profile", EditProfileView.as_view(), name="edit_profile"),
    path("offer_detail", OfferDetailView.as_view(), name="offer_detail"),
    path("edit_publish", PreEditView.as_view(), name="pre_edit_publish"),
    path("candidate", CandidateView.as_view(), name="candidates"),
    path("moderate_est", ModeratorEstView.as_view(), name="moderator_est"),
    path("moderate_comp", ModeratorCompView.as_view(), name="moderator_comp"),
]
