# DJANGO MODULES
from django.contrib import admin
from django.urls import path

# PROJECT MODULES
from .views import *

app_name = "offer_app"

urlpatterns = [
    # OFFERS
    path("list", OfferList.as_view(), name="offer_list"),
    path("create", OfferCreate.as_view(), name="offer_add"),
    path("detail/<slug:slug>", OfferDetail.as_view(), name="offer_detail"),
    path("modal/create", OfferModalCreate.as_view(), name="offer_modal_add"),
    path("modal/edit/<int:pk>", OfferEditModal.as_view(), name="offer_edit"),
    path("modal/delete/<int:pk>", OfferDeleteModal.as_view(), name="offer_delete"),
]
