from django.db import models
from django.db.models import Q, F, Count

from django.contrib.auth.models import BaseUserManager

class RulesManager(models.Manager):
    def get_nums(self):
        return self.annotate(
            num_apps=Count('app', distinct=True),
            num_roles=Count('role', distinct=True),
            num_restrictions=Count('restriction', distinct=True)
        ).order_by("id")