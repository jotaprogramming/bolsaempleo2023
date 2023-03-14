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


class UserGroups(models.Model):
    code = models.CharField(
        _("user group code"), max_length=3, unique=True, null=False
    )
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
        # abstract = True


class Policies(models.Model):
    usergroup = models.ForeignKey(
        UserGroups,
        related_name="usergroup_policy",
        verbose_name=_("usergroup"),
        blank=False,
        on_delete=models.PROTECT,
    )
    restriction = models.ManyToManyField(
        Restrictions,
        related_name="restriction_policies",
        verbose_name=_("restriction"),
        blank=True,
    )
    app = models.ManyToManyField(
        Apps, related_name="app_policies", verbose_name=_("app"), blank=False
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, null=False)
    updated_at = models.DateTimeField(
        _("updated at"), auto_now_add=False, editable=True, null=True
    )
    deleted_at = models.DateTimeField(
        _("deleted at"), auto_now_add=False, editable=True, null=True
    )

    objects = PolicyManager()

    def __str__(self):
        return "{}".format(self.usergroup.group_name)
    
    def get_restrictions(self):
        return self.restriction.all()
    
    def get_apps(self):
        return self.app.all()

    class Meta:
        verbose_name = _("policy")
        verbose_name_plural = _("policies")


class Roles(models.Model):
    code = models.CharField(
        _("role code"), max_length=3, unique=True, null=False
    )
    role_name = models.CharField(_("role name"), max_length=50, unique=True, null=False)
    description = models.TextField(_("description"), null=False)
    restriction = models.ManyToManyField(
        Restrictions,
        related_name="role_restriction",
        verbose_name=_("restriction"),
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
        return "{}".format(self.role_name)

    class Meta:
        verbose_name = _("role")
        verbose_name_plural = _("roles")


class Traits(models.Model):
    user = models.ForeignKey(
        User,
        related_name="user",
        verbose_name=_("user"),
        blank=False,
        on_delete=models.PROTECT,
    )
    usergroup = models.ForeignKey(
        UserGroups,
        related_name="usergroup_traits",
        verbose_name=_("user group"),
        blank=False,
        on_delete=models.PROTECT,
    )
    role = models.ForeignKey(
        Roles,
        related_name="role_traits",
        verbose_name=_("role"),
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
        return "{}".format(self.user.username)

    class Meta:
        verbose_name = _("trait")
        verbose_name_plural = _("traits")


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
