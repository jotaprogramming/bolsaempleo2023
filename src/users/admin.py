from django.contrib import admin

# Register your models here.
from users.models import *
from users.forms import *


@admin.register(UserGroups)
class UserGroupsAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(UserGroupPolicies)
class PolicyAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(Restrictions)
class RestrictionsAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(UserRules)
class UserRulesAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(Apps)
class AppAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(Entities)
class EntitiesAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(Works)
class WorkAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(PersonalLanguages)
class PersonalLanguagesAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(CurriculumVitae)
class CurriculumVitaeAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]
