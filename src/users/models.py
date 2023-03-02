from django.db import models
from .managers import *
from config.models import Cities, DocumentType

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.core.mail import send_mail
from django.template.defaultfilters import slugify

# Create your models here.
class UserGroups(models.Model):
    group_name = models.CharField(
        _("user group name"), max_length=50, unique=True, null=False
    )
    description = models.TextField(_("description"), null=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, null=False)
    updated_at = models.DateTimeField(
        _("updated at"), auto_now_add=False, editable=True, null=True
    )
    deleted_at = models.DateTimeField(
        _("deleted at"), auto_now_add=False, editable=True, null=True
    )

    def __str__(self):
        return "{}".format(self.group_name)

    class Meta:
        verbose_name = _("user group")
        verbose_name_plural = _("user groups")


class Restrictions(models.Model):
    code = models.CharField(_("code"), max_length=3, unique=True, null=False)
    name = models.CharField(_("name"), max_length=25, unique=True, null=False)
    description = models.TextField(_("description"), null=False)
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
        verbose_name = _("restriction")
        verbose_name_plural = _("restrictions")


class Apps(models.Model):
    name = models.CharField(_("name"), max_length=25, unique=True, null=False)
    route = models.CharField(_("route"), max_length=100, unique=True, null=False)
    description = models.TextField(_("description"), null=False)
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
        verbose_name = _("application")
        verbose_name_plural = _("applications")
        # abstract = True


class Roles(models.Model):
    role_name = models.CharField(_("role name"), max_length=50, unique=True, null=False)
    description = models.TextField(_("description"), null=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, null=False)
    updated_at = models.DateTimeField(
        _("updated at"), auto_now_add=False, editable=True, null=True
    )
    deleted_at = models.DateTimeField(
        _("deleted at"), auto_now_add=False, editable=True, null=True
    )

    def __str__(self):
        return "{}".format(self.role_name)

    class Meta:
        verbose_name = _("role")
        verbose_name_plural = _("roles")


class Rules(models.Model):
    # code = models.CharField(_("code"), max_length=6, unique=True, null=False)
    user = models.ForeignKey(
        User,
        related_name="user",
        verbose_name=_("user"),
        blank=False,
        on_delete=models.PROTECT,
    )
    app = models.ManyToManyField(
        Apps, related_name="app_rule", verbose_name=_("app"), blank=False
    )
    restriction = models.ManyToManyField(
        Restrictions,
        related_name="restriction_rule",
        verbose_name=_("restriction"),
        blank=True,
    )
    role = models.ManyToManyField(
        Roles, related_name="role_rule", verbose_name=_("role"), blank=False
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, null=False)
    updated_at = models.DateTimeField(
        _("updated at"), auto_now_add=False, editable=True, null=True
    )
    deleted_at = models.DateTimeField(
        _("deleted at"), auto_now_add=False, editable=True, null=True
    )

    objects = RulesManager()

    class Meta:
        verbose_name = _("rule")
        verbose_name_plural = _("rules")


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="user_profile_user",
        verbose_name=_("user"),
        blank=False,
        on_delete=models.PROTECT,
    )
    slug = models.SlugField(max_length=120, unique=True)
    document_type = models.ForeignKey(
        DocumentType,
        related_name="user_document_type",
        verbose_name=_("document type"),
        blank=False,
        on_delete=models.PROTECT,
    )
    id_number = models.CharField(
        _("user identification number"), max_length=25, null=False
    )
    name = models.CharField(_("user's short name"), max_length=100, blank=True)
    phone = models.CharField(_("cell phone number"), max_length=25, blank=False)
    email = models.EmailField(_("contact e-mail address"), max_length=250, blank=False)
    address = models.CharField(
        _("address of residence or work stay"), max_length=250, blank=False
    )
    city = models.ForeignKey(
        Cities,
        related_name="user_city",
        verbose_name=_("city"),
        blank=False,
        on_delete=models.PROTECT,
    )
    about_me = models.TextField(_("About Me"), blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, null=False)
    updated_at = models.DateTimeField(
        _("updated at"), auto_now_add=False, editable=True, null=True
    )
    deleted_at = models.DateTimeField(
        _("deleted at"), auto_now_add=False, editable=True, null=True
    )

    def __str__(self):
        return "{}".format(self.user.username)

    def slug(self):
        return slugify(self.user.username)

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")


class CurriculumVitae(models.Model):
    userprofile = models.OneToOneField(
        UserProfile,
        related_name="user_cv",
        verbose_name=_("user profile"),
        blank=True,
        on_delete=models.PROTECT,
    )
    cv_path = models.TextField(_("path"), null=False)

    def __str__(self):
        return "{}".format(self.userprofile.user.username)

    class Meta:
        verbose_name = _("curriculum vitae")
        verbose_name_plural = _("curriculum vitae")
