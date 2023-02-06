from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserGroups(models.Model):
    group_name = models.CharField(max_length=50, unique=True, null=False)
    description = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=False, editable=True, null=True)
    deleted_at = models.DateTimeField(auto_now_add=False, editable=True, null=True)


class Restrictions(models.Model):
    code = models.CharField(max_length=3, unique=True, null=False)
    name = models.CharField(max_length=25, unique=True, null=False)
    description = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=False, editable=True, null=True)
    deleted_at = models.DateTimeField(auto_now_add=False, editable=True, null=True)


class Apps(models.Model):
    name = models.CharField(max_length=25, unique=True, null=False)
    route = models.CharField(max_length=100, unique=True, null=False)
    description = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=False, editable=True, null=True)
    deleted_at = models.DateTimeField(auto_now_add=False, editable=True, null=True)


class Roles(models.Model):
    role_name = models.CharField(max_length=50, unique=True, null=False)
    description = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=False, editable=True, null=True)
    deleted_at = models.DateTimeField(auto_now_add=False, editable=True, null=True)


class Rules(models.Model):
    app = models.ManyToManyField(Apps, related_name="app_rule", blank=False)
    restriction = models.ManyToManyField(
        Restrictions,
        related_name="restriction_rule",
        blank=False,
    )
    role = models.ManyToManyField(
        Roles, related_name="role_rule", blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=False, editable=True, null=True)
    deleted_at = models.DateTimeField(auto_now_add=False, editable=True, null=True)


class Users(models.Model):
    group = models.OneToOneField(
        UserGroups, related_name="user_group", blank=False, on_delete=models.PROTECT
    )
    rule = models.OneToOneField(
        Roles, related_name="user_rule", blank=False, on_delete=models.PROTECT
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=False, editable=True, null=True)
    deleted_at = models.DateTimeField(auto_now_add=False, editable=True, null=True)
