# DJANGO MODULES
from django.contrib import admin
from django.urls import path

# PROJECT MODULES
from .views import *

app_name = "users_app"

urlpatterns = [
    # USER GROUPS
    path("user/group/list", UserGroupList.as_view(), name="usergroup_list"),
    path("user/group/add", UserGroupCreate.as_view(), name="usergroup_add"),
    path(
        "user/group/edit/<int:pk>",
        UserGroupEditModal.as_view(),
        name="usergroup_edit",
    ),
    path(
        "user/group/delete/<int:pk>",
        UserGroupDeleteModal.as_view(),
        name="usergroup_delete",
    ),
    # RESTRICTIONS
    path(
        "user/restriction/list",
        RestrictionList.as_view(),
        name="restriction_list",
    ),
    path(
        "user/restriction/add",
        RestrictionCreate.as_view(),
        name="restriction_add",
    ),
    path(
        "user/restriction/edit/<int:pk>",
        RestrictionEditModal.as_view(),
        name="restriction_edit",
    ),
    path(
        "user/restriction/delete/<int:pk>",
        RestrictionDeleteModal.as_view(),
        name="restriction_delete",
    ),
    # APPS
    path("user/app/list", AppList.as_view(), name="app_list"),
    path(
        "user/app/edit/<int:pk>",
        AppEditModal.as_view(),
        name="app_edit",
    ),
    # ROLES
    path("user/role/list", RoleList.as_view(), name="role_list"),
    path("user/role/add", RoleCreate.as_view(), name="role_add"),
    path("user/role/edit/<int:pk>", RoleEditModal.as_view(), name="role_edit"),
    path(
        "user/role/delete/<int:pk>",
        RoleDeleteModal.as_view(),
        name="role_delete",
    ),
    # RULES
    path("user/rule/list", RuleList.as_view(), name="rule_list"),
    path("user/rule/add", RuleCreate.as_view(), name="rule_add"),
    path("user/rule/edit/<int:pk>", RuleEditModal.as_view(), name="rule_edit"),
    path(
        "user/rule/delete/<int:pk>",
        RuleDeleteModal.as_view(),
        name="rule_delete",
    ),
    # USERS
    path("user/list", UserList.as_view(), name="user_list"),
    path("user/add", UserCreate.as_view(), name="user_add"),
    path("user/edit/<int:pk>", UserEditModal.as_view(), name="user_edit"),
    path("user/delete/<int:pk>", UserDeleteModal.as_view(), name="user_delete"),
    # LOG
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", UserLogout.as_view(), name="logout"),
]
