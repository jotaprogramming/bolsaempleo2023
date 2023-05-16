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
    # POLICY
    path("user/policy/list", PolicyList.as_view(), name="policy_list"),
    path("user/policy/add", PolicyCreate.as_view(), name="policy_add"),
    path("user/policy/edit/<int:pk>", PolicyEditModal.as_view(), name="policy_edit"),
    path(
        "user/policy/delete/<int:pk>",
        PolicyDeleteModal.as_view(),
        name="policy_delete",
    ),
    # USER RULES
    path("user/rule/list", UserRulesList.as_view(), name="rule_list"),
    path("user/rule/add", UserRulesCreate.as_view(), name="rule_add"),
    path("user/rule/edit/<int:pk>", UserRulesEditModal.as_view(), name="rule_edit"),
    path(
        "user/rule/delete/<int:pk>",
        UserRulesDeleteModal.as_view(),
        name="rule_delete",
    ),
    # USERS
    path("user/list", UserList.as_view(), name="user_list"),
    path("user/add", UserCreate.as_view(), name="user_add"),
    path("user/edit/<int:pk>", UserEditModal.as_view(), name="user_edit"),
    path("user/delete/<int:pk>", UserDeleteModal.as_view(), name="user_delete"),
    # LOG
    path("login/", UserLogin.as_view(), name="login"),
    path("logout", UserLogout.as_view(), name="logout"),
    # path("register", RegisterView.as_view(), name="register"),
    path("register/choices", PreRegisterView.as_view(), name="register_choices"),
    path("register/student", RegisterStudentView.as_view(), name="register_student"),
    path("register/company", RegisterCompanyView.as_view(), name="register_company"),
    path(
        "credentials/recover",
        CredentialsRecoverView.as_view(),
        name="credentials_recover",
    ),
    # USER PROFILE
    path("profile/<slug:slug>", UserProfileDetail.as_view(), name="userprofile"),
    path(
        "profile/<slug:slug>/add",
        UserProfileCreate.as_view(),
        name="userprofile_add",
    ),
    path(
        "profile/<slug:slug>/edit",
        UserProfileEdit.as_view(),
        name="userprofile_edit",
    ),
    # CURRICULUM VITAE
    # path("curriculum/<slug:slug>", CurriculumVitaeDetail.as_view(), name="userprofile"),
    path(
        "curriculum/<slug:slug>/add",
        CurriculumVitaeCreate.as_view(),
        name="cv_add",
    ),
    path(
        "curriculum/<slug:slug>/edit",
        CurriculumVitaeEdit.as_view(),
        name="cv_edit",
    ),
    path(
        "curriculum/<slug:slug>/delete/attached",
        CurriculumVitaeDeleteAttached.as_view(),
        name="cv_delete_attached",
    ),
]
