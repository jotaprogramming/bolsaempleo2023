# DJANGO MODULES
from django.contrib import admin
from django.urls import path

# PROJECT MODULES
from .views import *

app_name = "users_app"

urlpatterns = [
    # USER GROUPS
    path("group/list", UserGroupList.as_view(), name="usergroup_list"),
    path("group/add", UserGroupCreate.as_view(), name="usergroup_add"),
    path("group/edit/<int:pk>", UserGroupEditModal.as_view(), name="usergroup_edit"),
    path(
        "group/delete/<int:pk>", UserGroupDeleteModal.as_view(), name="usergroup_delete"
    ),
    # RESTRICTIONS
    path("restriction/list", RestrictionList.as_view(), name="restriction_list"),
    path("restriction/add", RestrictionCreate.as_view(), name="restriction_add"),
    path(
        "restriction/edit/<int:pk>",
        RestrictionEditModal.as_view(),
        name="restriction_edit",
    ),
    path(
        "restriction/delete/<int:pk>",
        RestrictionDeleteModal.as_view(),
        name="restriction_delete",
    ),
]
