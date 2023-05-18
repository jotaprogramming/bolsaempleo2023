from django.db import models
from django.db.models import Q, F, Count

from django.contrib.auth.models import BaseUserManager


class OffersManager(models.Manager):
    def search(self, text="", order="id"):
        """
        This function searches for objects based on various fields and orders the results by a specified
        field.
        
        :param text: The search query text that the function will use to filter the results
        :param order: The order parameter specifies the field by which the search results should be
        ordered. By default, the search results are ordered by the "id" field. However, the user can
        specify a different field to order the results, defaults to id (optional)
        :return: A search function that takes in a text string and an order string as parameters and
        returns a filtered queryset of objects based on the text parameter and ordered by the order
        parameter. The function searches for objects that have a user first name, title, currency iso or
        name, city name, district name or country name, contract type name, workday name, or pay period
        name that contains the text parameter.
        """

        # This code checks if the string "true" is present in the `text` parameter. If it is, it
        # removes the string "true" from the `text` parameter by replacing it with an empty string.
        if "true" in text:
            text = text.replace("true", "")

        # This code block checks if the "#" character is present in the `text` parameter. If it is, it
        # replaces the "#" character with an empty string and filters the queryset of objects based on
        # the `tags__name` field that contains the modified `text` parameter. Finally, it orders the
        # results by the "id" field and returns the filtered queryset. This code block is used to
        # search for objects based on a specific tag.
        if "#" in text:
            text = text.replace("#", "")
            return self.all().filter(tags__name__in=[text]).order_by("id")

        return (
            self.all()
            .filter(
                Q(user__first_name__icontains=text)
                | Q(title__icontains=text)
                | Q(currency__iso__icontains=text)
                | Q(currency__name__icontains=text)
                | Q(city__name__icontains=text)
                | Q(city__district__name__icontains=text)
                | Q(city__district__country__name__icontains=text)
                | Q(conttype__name__icontains=text)
                | Q(workday__name__icontains=text)
                | Q(payperiod__name__icontains=text)
            )
            .order_by(order)
        )
