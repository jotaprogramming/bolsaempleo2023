# DJANGO MODULES
from django.contrib import admin
from django.urls import path

# PROJECT MODULES
from .views import *

app_name = "offer_app"

urlpatterns = [
    # OFFERS
    path("list", OfferList.as_view(), name="offer_list"),
    path("panel", BiddingPanel.as_view(), name="bidding_panel"),
    path("publish", PublicationCreate.as_view(), name="offer_add"),
    path("update/<slug:slug>", PublicationEdit.as_view(), name="offer_edit"),
    path("detail/<slug:slug>", OfferDetail.as_view(), name="offer_detail"),
    path("modal/create", OfferModalCreate.as_view(), name="offer_modal_add"),
    path("modal/edit/<int:pk>", OfferEditModal.as_view(), name="offer_edit"),
    path("modal/delete/<int:pk>", OfferDeleteModal.as_view(), name="offer_delete"),
    path(
        "<str:username>/publications", PublicationList.as_view(), name="mypublications"
    ),
    # CANDIDATURES
    path("candidatures/list", CandidaturesList.as_view(), name="candidature_list"),
    path(
        "<slug:slug>/candidatures/list",
        CandidaturesByOfferList.as_view(),
        name="candidature_list",
    ),
    path(
        "candidatures/<str:username>/list",
        MyCandidacies.as_view(),
        name="mycandidacies",
    ),
    path(
        "<str:slug>/candidatures/save/<str:username>",
        CandidatureSave.as_view(),
        name="candidature_save",
    ),
    path(
        "candidatures/modal/edit/<int:pk>",
        CandidatureEditModal.as_view(),
        name="candidature_edit",
    ),
    path(
        "candidatures/modal/delete/<int:pk>",
        CandidatureDeleteModal.as_view(),
        name="candidature_delete",
    ),
]
