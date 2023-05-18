from django.db import models
from django.db.models import Q, F, Count

from django.contrib.auth.models import BaseUserManager


class PolicyManager(models.Manager):
    def get_nums(self):
        """
        This function returns a queryset of objects annotated with the count of distinct related objects
        and ordered by their id.
        :return: The `get_nums` method is returning a queryset that has been annotated with two
        additional fields: `num_restrictions` and `num_apps`. These fields represent the count of
        distinct `Restriction` and `App` objects related to each instance of the queryset. The queryset
        is also ordered by the `id` field.
        """
        return self.annotate(
            num_restrictions=Count("restriction", distinct=True),
            num_apps=Count("app", distinct=True),
        ).order_by("id")
