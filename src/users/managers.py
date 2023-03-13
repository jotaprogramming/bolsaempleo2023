from django.db import models
from django.db.models import Q, F, Count

from django.contrib.auth.models import BaseUserManager


class PolicyManager(models.Manager):
    def get_nums(self):
        return self.annotate(
            num_restrictions=Count("restriction", distinct=True),
            num_apps=Count("app", distinct=True),
        ).order_by("id")
