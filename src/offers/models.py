from django.db import models

# from .managers import *
from config.models import Countries, Currencies, Cities, DocumentType

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.core.mail import send_mail
from django.template.defaultfilters import slugify

from .utils import string_to_base64


# Create your models here.
class Tags(models.Model):
    name = models.CharField(_("name"), max_length=15, unique=True, null=False)

    def __str__(self):
        return "{}".format(self.name)

    def slug(self):
        return slugify(self.name)

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")


class Requirements(models.Model):
    name = models.CharField(_("name"), max_length=50, null=False)

    def __str__(self):
        return "{}".format(self.name)

    def slug(self):
        return slugify(self.name)

    class Meta:
        verbose_name = _("requirement")
        verbose_name_plural = _("requirements")


class Workdays(models.Model):
    name = models.CharField(_("name"), max_length=50, null=False)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = _("workday")
        verbose_name_plural = _("workdays")


class PayPeriods(models.Model):
    name = models.CharField(_("name"), max_length=25, null=False)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = _("pay period")
        verbose_name_plural = _("pay periods")


class PostStatus(models.Model):
    name = models.CharField(_("name"), max_length=25, null=False)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = _("postulation status")
        verbose_name_plural = _("postulation statuses")


class Modalities(models.Model):
    name = models.CharField(_("name"), max_length=25, null=False)
    description = models.TextField(_("description"), null=False)
    country = models.ForeignKey(
        Countries,
        related_name="country_modality",
        verbose_name=_("country"),
        blank=False,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = _("modality")
        verbose_name_plural = _("modalities")


class ContractTypes(models.Model):
    name = models.CharField(_("name"), max_length=50, null=False)
    country = models.ForeignKey(
        Countries,
        related_name="country_contract_type",
        verbose_name=_("country"),
        blank=False,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = _("contract type")
        verbose_name_plural = _("contract types")


class Offers(models.Model):
    user = models.ForeignKey(
        User,
        related_name="offer_user",
        verbose_name=_("user"),
        blank=False,
        on_delete=models.PROTECT,
    )
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(_("title"), max_length=255, null=False)
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False
    )
    currency = models.ForeignKey(
        Currencies,
        related_name="offer_currency",
        verbose_name=_("currency"),
        blank=False,
        on_delete=models.PROTECT,
    )
    vacancies = models.IntegerField(default=0, blank=True, null=True)
    modality = models.ForeignKey(
        Modalities,
        related_name="offer_modality",
        verbose_name=_("modality"),
        blank=False,
        on_delete=models.PROTECT,
    )
    city = models.ForeignKey(
        Cities,
        related_name="offer_city",
        verbose_name=_("city"),
        blank=False,
        on_delete=models.PROTECT,
    )
    hiring_date = models.DateField(auto_now_add=False, editable=True, null=True)
    conttype = models.ForeignKey(
        ContractTypes,
        related_name="offer_contract_type",
        verbose_name=_("contract type"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    workday = models.ForeignKey(
        Workdays,
        related_name="offer_workday",
        verbose_name=_("workday"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    payperiod = models.ForeignKey(
        PayPeriods,
        related_name="offer_payperiod",
        verbose_name=_("pay period"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    description = models.TextField(_("description"), null=False)
    requirements = models.ManyToManyField(
        Requirements,
        related_name="offers_requirements",
        verbose_name=_("requirements"),
        blank=True,
    )
    tags = models.ManyToManyField(
        Tags,
        related_name="offers_tags",
        verbose_name=_("tags"),
        blank=True,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, null=False)
    updated_at = models.DateTimeField(
        _("updated at"), auto_now_add=False, editable=True, null=True
    )
    deleted_at = models.DateTimeField(
        _("deleted at"), auto_now_add=False, editable=True, null=True
    )

    def __str__(self):
        return "{}".format(self.title)

    def slug(self):
        # _b = string_to_base64(str(self.pk))
        _b = self.pk
        _field = f"{self.title} {_b}"
        return slugify(_field)

    def get_requirements(self):
        if self.requirements:
            return self.requirements.all()

    def get_tags(self):
        if self.tags:
            return self.tags.all()

    class Meta:
        verbose_name = _("offer")
        verbose_name_plural = _("offers")


class Candidatures(models.Model):
    offer = models.ForeignKey(
        Offers,
        related_name="candidature_offer",
        verbose_name=_("offer"),
        blank=False,
        on_delete=models.PROTECT,
    )
    status = models.ForeignKey(
        PostStatus,
        related_name="candidature_status",
        verbose_name=_("status"),
        blank=False,
        on_delete=models.PROTECT,
    )
    candidate = models.ForeignKey(
        User,
        related_name="candidate",
        verbose_name=_("candidate"),
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
        return "{}".format(self.candidate.username)

    class Meta:
        verbose_name = _("candidature")
        verbose_name_plural = _("candidatures")
