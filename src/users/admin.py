from django.contrib import admin

# Register your models here.
from users.models import *
from users.forms import *


@admin.register(UserGroups)
class UserGroupsAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(Restrictions)
class RestrictionsAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(Rules)
class RulesAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(Apps)
class AppAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(CurriculumVitae)
class CurriculumVitaeAdmin(admin.ModelAdmin):
    exclude = []
