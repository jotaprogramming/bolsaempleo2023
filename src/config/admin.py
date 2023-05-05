from django.contrib import admin

# Register your models here.
from .models import *

# from .forms import *


@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(Districts)
class DistrictsAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(Currencies)
class CurrenciesAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(Languages)
class LanguagesAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(Specializations)
class SpecializationsAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(Workdays)
class WorkdaysAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(PayPeriods)
class PayPeriodsAdmin(admin.ModelAdmin):
    exclude = []


# @admin.register(POST_STATUS)
# class PostStatusAdmin(admin.ModelAdmin):
#     exclude = []


@admin.register(Modalities)
class ModalitiesAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(ContractTypes)
class ContractTypesAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    exclude = []
