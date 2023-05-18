# DJANGO MODULES
from django.contrib import admin
from django.urls import path

# PROJECT MODULES
from reports.views import *

app_name = "reports_app"

urlpatterns = [
    path("home", ReportsHome.as_view(), name="reports_home"),
    path("users", UserReport.as_view(), name="user_report"),
    path("offers", OfferReport.as_view(), name="offer_report"),
]
