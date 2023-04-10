from django.contrib import admin

from offers.models import *


# Register your models here.
@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(Requirements)
class RequirementsAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(Offers)
class OffersAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(Candidatures)
class CandidaturesAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]
