# DJANGO MODULES
from django.contrib import admin
from django.urls import path

# PROJECT MODULES
from .views import *

app_name = "offers_app"

urlpatterns = [
    # OFFERS
    path("list", OfferList.as_view(), name="offer_list"),
    path("panel", BiddingPanel.as_view(), name="bidding_panel"),
    path("publish", PublicationCreate.as_view(), name="offer_add"),
    path("update/<slug:slug>", PublicationEdit.as_view(), name="offer_edit"),
    path("detail/<slug:slug>", OfferDetail.as_view(), name="offer_detail"),
    path("modal/create", OfferModalCreate.as_view(), name="offer_modal_add"),
    path("modal/edit/<int:pk>", OfferEditModal.as_view(), name="offer_edit"),
    path("modal/delete/<slug:slug>", OfferDeleteModal.as_view(), name="offer_delete"),
    path("modal/finish/<slug:slug>", OfferFinishModal.as_view(), name="offer_finish"),
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
        CandidatureStatusEdit.as_view(),
        name="candidature_status_edit",
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
