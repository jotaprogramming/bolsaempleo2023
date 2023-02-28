from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Countries(models.Model):
    iso = models.CharField(
        _("ISO 3166-1 alpha-2 code of the country"), max_length=5, unique=True, null=False
    )
    name = models.CharField(
        _("common country name"), max_length=150, unique=False, null=False
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, null=False)
    updated_at = models.DateTimeField(
        _("updated at"), auto_now_add=False, editable=True, null=True
    )
    deleted_at = models.DateTimeField(
        _("deleted at"), auto_now_add=False, editable=True, null=True
    )

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = _("country")
        verbose_name_plural = _("countries")
    

class Districts(models.Model):
    iso = models.CharField(
        _("ISO 3166-2 of administrative subdivision"), max_length=5, unique=True, null=False
    )
    zipcode = models.CharField(
        _("administrative subdivision zip code"), max_length=25, unique=True, null=False
    )
    name = models.CharField(
        _("common name of the administrative subdivision"), max_length=150, unique=False, null=False
    )
    country = models.ForeignKey(
        Countries,
        related_name="country_district",
        verbose_name=_("country"),
        blank=False,
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, null=False)
    updated_at = models.DateTimeField(
        _("updated at"), auto_now_add=False, editable=True, null=True
    )
    deleted_at = models.DateTimeField(
        _("deleted at"), auto_now_add=False, editable=True, null=True
    )

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = _("district")
        verbose_name_plural = _("districts")
    

class Cities(models.Model):
    zipcode = models.CharField(
        _("city zip code"), max_length=25, unique=True, null=False
    )
    name = models.CharField(
        _("common name of the city"), max_length=150, unique=False, null=False
    )
    district = models.ForeignKey(
        Districts,
        related_name="city_district",
        verbose_name=_("district"),
        blank=False,
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, null=False)
    updated_at = models.DateTimeField(
        _("updated at"), auto_now_add=False, editable=True, null=True
    )
    deleted_at = models.DateTimeField(
        _("deleted at"), auto_now_add=False, editable=True, null=True
    )

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")
    

class Currencies(models.Model):
    iso = models.CharField(
        _("ISO 4217 of a country's currency"), max_length=5, unique=True, null=False
    )
    name = models.CharField(
        _("name of the currency"), max_length=100, unique=False, null=False
    )
    country = models.ManyToManyField(
        Countries,
        related_name="currency_country",
        verbose_name=_("country"),
        blank=False,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, null=False)
    updated_at = models.DateTimeField(
        _("updated at"), auto_now_add=False, editable=True, null=True
    )
    deleted_at = models.DateTimeField(
        _("deleted at"), auto_now_add=False, editable=True, null=True
    )

    def __str__(self):
        return "{}".format(self.iso)

    class Meta:
        verbose_name = _("currency")
        verbose_name_plural = _("currencies")
    

class DocumentType(models.Model):
    acronym = models.CharField(
        _("document type acronym"), max_length=10, unique=False, null=False
    )
    name = models.CharField(
        _("name of document type"), max_length=100, unique=False, null=False
    )
    country = models.ManyToManyField(
        Countries,
        related_name="document_type_country",
        verbose_name=_("country"),
        blank=False,
    )

    def __str__(self):
        return "{}".format(self.acronym)

    class Meta:
        verbose_name = _("document type")
        verbose_name_plural = _("document types")