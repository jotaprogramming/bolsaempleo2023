# DJANGO MODULES
from django.contrib import admin
from django.urls import path

# PROJECT MODULES
from .views import *

app_name = "users_app"

urlpatterns = [
    path("list", UserGroupList.as_view(), name="usergroup_list"),
    path("add", UserGroupCreate.as_view(), name="usergroup_add"),
    path("edit/<int:pk>", UserGroupEditModal.as_view(), name="usergroup_edit"),
    path("delete/<int:pk>", UserGroupDeleteModal.as_view(), name="usergroup_delete"),
]
