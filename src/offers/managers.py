from django.db import models
from django.db.models import Q, F, Count

from django.contrib.auth.models import BaseUserManager


class OffersManager(models.Manager):
    def search(self, text='', order='id'):
        if 'true' in text:
            text = text.replace('true', '')

        if '#' in text:
            text = text.replace('#', '')
            return self.all().filter(
                tags__name__in=[text]
            ).order_by("id")

        return self.all().filter(
            Q(user__first_name__icontains=text) |
            Q(title__icontains=text) |
            Q(currency__iso__icontains=text) |
            Q(currency__name__icontains=text) |
            Q(city__name__icontains=text) |
            Q(city__district__name__icontains=text) |
            Q(city__district__country__name__icontains=text) |
            Q(conttype__name__icontains=text) |
            Q(workday__name__icontains=text) |
            Q(payperiod__name__icontains=text)
        ).order_by(order)
