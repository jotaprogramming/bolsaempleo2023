# PROJECT MODULES
from users.models import *
from core.utils import *
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


def diplicate_usergroups(self, form):
    """
    If the user is editing an existing group, exclude that group from the query. Then, if the group name
    already exists, return the count of groups with that name

    :param form: The form instance
    :return: The count of the number of groups with the same name.
    """
    _id = self.kwargs.get("pk", None)
    groups = UserGroups.objects.all()

    if _id:
        groups = groups.exclude(id=_id)

    group_name = form.instance.group_name
    count = groups.filter(group_name__exact=group_name).count()
    return count


def diplicate_restrictions(self, form):
    """
    It returns the number of times the code and name of the restriction being created or edited already
    exist in the database

    :param form: The form instance that is being validated
    :return: A tuple of two integers.
    """
    _id = self.kwargs.get("pk", None)
    restrictions = Restrictions.objects.all()

    if _id:
        restrictions = restrictions.exclude(id=_id)

    code = form.instance.code
    name = form.instance.name
    count_code = restrictions.filter(code__exact=code).count()
    count_name = restrictions.filter(name__exact=name).count()
    return count_code, count_name


def diplicate_apps(self, form):
    """
    It returns the number of apps that have the same name and route as the app being created or updated.

    :param form: The form instance that was submitted
    :return: A tuple of two integers.
    """
    _id = self.kwargs.get("pk", None)
    apps = Apps.objects.all()

    if _id:
        apps = apps.exclude(id=_id)

    name = form.instance.name
    route = form.instance.route
    count_name = apps.filter(name__exact=name).count()
    count_route = apps.filter(route__exact=route).count()
    return count_name, count_route
