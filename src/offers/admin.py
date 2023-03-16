from django.contrib import admin

from offers.models import *


# Register your models here.
@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(Requirements)
class RequirementsAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(Workdays)
class WorkdaysAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(PayPeriods)
class PayPeriodsAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(PostStatus)
class PostStatusAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(Modalities)
class ModalitiesAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(ContractTypes)
class ContractTypesAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(Offers)
class OffersAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(Candidatures)
class CandidaturesAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]
