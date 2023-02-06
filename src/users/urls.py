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
    # APPS
    path("app/list", AppList.as_view(), name="app_list"),
    path(
        "app/edit/<int:pk>",
        AppEditModal.as_view(),
        name="app_edit",
    ),
    # ROLES
    path("role/list", RoleList.as_view(), name="role_list"),
    path("role/add", RoleCreate.as_view(), name="role_add"),
    path("role/edit/<int:pk>", RoleEditModal.as_view(), name="role_edit"),
    path(
        "role/delete/<int:pk>", RoleDeleteModal.as_view(), name="role_delete"
    ),
    # RULES
    path("rule/list", RuleList.as_view(), name="rule_list"),
    path("rule/add", RuleCreate.as_view(), name="rule_add"),
    path("rule/edit/<int:pk>", RuleEditModal.as_view(), name="rule_edit"),
    path(
        "rule/delete/<int:pk>", RuleDeleteModal.as_view(), name="rule_delete"
    ),
]
