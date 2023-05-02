from PIL import Image

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.core.mail import send_mail
from django.template.defaultfilters import slugify

from .managers import *
from .validators import validate_document, validate_image
from config.models import Cities, DocumentType, Languages, Specializations


# Choices
STUDY_LEVEL = (
    ("1", "Educación básica - Primaria"),
    ("2", "Educación básica - Secundaria"),
    ("3", "Educación media - Bachillerato"),
    ("4", "Educación superioa - Carrera técnica"),
    ("5", "Educación superioa - Carrera tecnológica"),
    ("6", "Educación superioa - Carrera profesional"),
    ("7", "Postgrada - Especialización"),
    ("8", "Postgrada - Maestría"),
    ("9", "Postgrada - Doctorado"),
)

LAN_LEVEL = (
    ("1", "Muy básico"),
    ("2", "Básico"),
    ("3", "Intermedio"),
    ("4", "Avanzado"),
    ("5", "Nativo"),
)


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
    name = models.CharField(_("name"), max_length=100, unique=True, null=False)
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
    code = models.CharField(_("user group code"), max_length=3, unique=True, null=False)
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


class UserGroupPolicies(models.Model):
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
        verbose_name = _("user group policy")
        verbose_name_plural = _("user group policies")


class Roles(models.Model):
    code = models.CharField(_("role code"), max_length=3, unique=True, null=False)
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


class UserRules(models.Model):
    user = models.ForeignKey(
        User,
        related_name="rule_user",
        verbose_name=_("user"),
        blank=False,
        on_delete=models.PROTECT,
    )
    usergroup = models.ForeignKey(
        UserGroups,
        related_name="user_group",
        verbose_name=_("user group"),
        blank=False,
        on_delete=models.PROTECT,
    )
    role = models.ForeignKey(
        Roles,
        related_name="user_role",
        verbose_name=_("user role"),
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
        verbose_name = _("user rule")
        verbose_name_plural = _("user rules")


class UserProfile(models.Model):
    avatar = models.ImageField(
        verbose_name=_("avatar"),
        upload_to="profile/",
        blank=True,
        null=True,
        # validators=[validate_image],
    )
    user = models.OneToOneField(
        User,
        related_name="userprofile",
        verbose_name=_("user"),
        blank=False,
        on_delete=models.PROTECT,
    )
    web = models.TextField(_("web or social network"), null=True)
    # slug = models.SlugField(max_length=120, unique=True)
    document_type = models.ForeignKey(
        DocumentType,
        related_name="userprofile_document_type",
        verbose_name=_("document type"),
        blank=True,
        on_delete=models.PROTECT,
    )
    id_number = models.CharField(
        _("company identification number"), max_length=25, blank=True, null=False
    )
    phone = models.CharField(_("cell phone number"), max_length=25, blank=True)
    email = models.EmailField(_("contact e-mail"), max_length=250, blank=True)
    address = models.CharField(_("address"), max_length=250, blank=True)
    city = models.ForeignKey(
        Cities,
        related_name="userprofile_city",
        verbose_name=_("city"),
        blank=True,
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

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        if self.avatar:
            image = Image.open(self.avatar.path)
            # image.save(self.avatar.path, quality=20, optimize=True)
            # image = Image.open(self.post_image.path)
            maxsize = 500
            dim = image.width if image.width < image.height else image.height
            if dim > maxsize:
                per = maxsize / dim
                re_width = per * image.width
                re_height = per * image.height
                output_size = (re_width, re_height)
                image.thumbnail(output_size)

            # image.save(self.avatar.path)
            image.save(self.avatar.path, quality=20, optimize=True)
            return image

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")


class Personnel(models.Model):
    # picture = models.FileField(
    #     verbose_name=_("picture"),
    #     upload_to="pictures/",
    #     blank=True,
    #     null=True,
    #     validators=[validate_image],
    # )
    document_type = models.ForeignKey(
        DocumentType,
        related_name="personnel_document_type",
        verbose_name=_("document type"),
        blank=False,
        on_delete=models.PROTECT,
    )
    id_number = models.CharField(_("identification number"), max_length=25, null=False)
    fullname = models.CharField(_("fullname"), max_length=100, unique=True, null=False)
    # position = models.CharField(
    #     _("position or specialization of the individual"), max_length=100, blank=False
    # )
    specialization = models.ForeignKey(
        Specializations,
        related_name="specializations",
        verbose_name=_("specialization"),
        blank=False,
        on_delete=models.PROTECT,
    )
    # phone = models.CharField(_("cell phone number"), max_length=25, blank=False)
    # email = models.EmailField(_("contact e-mail address"), max_length=250, blank=False)
    # address = models.CharField(_("residence address"), max_length=250, blank=True)
    # city = models.ForeignKey(
    #     Cities,
    #     related_name="personnel_city",
    #     verbose_name=_("city"),
    #     blank=False,
    #     on_delete=models.PROTECT,
    # )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, null=False)
    updated_at = models.DateTimeField(
        _("updated at"), auto_now_add=False, editable=True, null=True
    )
    deleted_at = models.DateTimeField(
        _("deleted at"), auto_now_add=False, editable=True, null=True
    )

    def __str__(self):
        return "{}".format(self.fullname)

    class Meta:
        verbose_name = _("personnel")
        verbose_name_plural = _("personnel")


class Companies(models.Model):
    userprofile = models.OneToOneField(
        UserProfile,
        related_name="company_profile",
        verbose_name=_("company profile"),
        blank=False,
        on_delete=models.PROTECT,
    )
    personnel = models.ManyToManyField(
        Personnel,
        related_name="company_personnel",
        verbose_name=_("company personnel"),
        blank=True,
    )
    name = models.CharField(_("company name"), max_length=100, null=False)

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
        verbose_name = _("company")
        verbose_name_plural = _("companies")


class Entities(models.Model):
    company = models.ForeignKey(
        Companies,
        related_name="company_entity",
        verbose_name=_("company"),
        blank=True,
        on_delete=models.PROTECT,
    )
    another_name = models.CharField(_("other name"), max_length=100, null=True)
    start_date = models.DateField(
        _("start date"), auto_now_add=False, editable=True, null=True
    )
    end_date = models.DateField(
        _("end date"), auto_now_add=False, editable=True, null=True
    )
    currently = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.another_name)

    class Meta:
        verbose_name = _("entity")
        verbose_name_plural = _("entities")


class CurriculumVitae(models.Model):
    userprofile = models.OneToOneField(
        UserProfile,
        related_name="user_cv",
        verbose_name=_("user profile"),
        blank=False,
        on_delete=models.PROTECT,
    )
    specialization = models.ForeignKey(
        Specializations,
        related_name="cv_specialization",
        verbose_name=_("specialization"),
        blank=False,
        on_delete=models.PROTECT,
    )
    # job_profile = models.TextField(_("job profile"), null=False)
    skills = models.TextField(_("skills"), null=True)
    attached = models.FileField(
        verbose_name=_("attached"),
        upload_to="cv/",
        blank=True,
        null=True,
        validators=[validate_document],
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, null=False)
    updated_at = models.DateTimeField(
        _("updated at"), auto_now_add=False, editable=True, null=True
    )
    deleted_at = models.DateTimeField(
        _("deleted at"), auto_now_add=False, editable=True, null=True
    )

    def __str__(self):
        return "{}".format(self.userprofile.user.username)

    class Meta:
        verbose_name = _("curriculum vitae")
        verbose_name_plural = _("curriculum vitae")


class Works(models.Model):
    cv = models.ForeignKey(
        CurriculumVitae,
        related_name="cv_works",
        verbose_name=_("cv work"),
        blank=False,
        on_delete=models.PROTECT,
    )
    company = models.ForeignKey(
        Entities,
        related_name="work_company",
        verbose_name=_("company"),
        blank=False,
        on_delete=models.PROTECT,
    )
    rating = models.DecimalField(
        _("rating"), max_digits=4, decimal_places=1, blank=True, null=True
    )
    performances = models.TextField(_("performances"), null=True)

    def __str__(self):
        return "{}".format(self.company.another_name)

    class Meta:
        verbose_name = _("work")
        verbose_name_plural = _("works")


class Education(models.Model):
    cv = models.ForeignKey(
        CurriculumVitae,
        related_name="cv_education",
        verbose_name=_("cv education"),
        blank=False,
        on_delete=models.PROTECT,
    )
    academy = models.ForeignKey(
        Entities,
        related_name="academy",
        verbose_name=_("academy"),
        blank=False,
        on_delete=models.PROTECT,
    )
    level = models.CharField(
        _("education level"), max_length=2, null=False, choices=STUDY_LEVEL
    )

    def __str__(self):
        return "{}".format(self.academy.another_name)

    class Meta:
        verbose_name = _("education")
        verbose_name_plural = _("educations")


class PersonalLanguages(models.Model):
    cv = models.ForeignKey(
        CurriculumVitae,
        related_name="cv_languages",
        verbose_name=_("cv languages"),
        blank=False,
        on_delete=models.PROTECT,
    )
    language = models.ForeignKey(
        Languages,
        related_name="language",
        verbose_name=_("language"),
        blank=False,
        on_delete=models.PROTECT,
    )
    level = models.CharField(
        _("language level"), max_length=1, null=False, choices=LAN_LEVEL
    )

    def __str__(self):
        return "{}".format(self.cv.userprofile.charge)

    class Meta:
        verbose_name = _("personal language")
        verbose_name_plural = _("personal languages")
