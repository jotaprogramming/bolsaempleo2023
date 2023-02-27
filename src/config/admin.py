from django.contrib import admin

# Register your models here.
from .models import *

# from .forms import *


@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(Districts)
class DistrictsAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(Currencies)
class CurrenciesAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    exclude = []
