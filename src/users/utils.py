# PROJECT MODULES
import re
from users.models import *
from core.utils import *
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.decorators.debug import sensitive_variables
from unicodedata import normalize


def format_diacritics(text):
    """
    The function removes diacritics from a given text string in Python.

    :param text: a string of text that may contain diacritics (accent marks, etc.)
    :return: The function `format_diacritics` returns a string with diacritics (accent marks) normalized
    to their base characters.
    """
    text = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+",
        r"\1",
        normalize("NFD", text),
        0,
        re.I,
    )
    return normalize("NFC", text)


def duplicate_usergroups(self, form):
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

    code = form.instance.code
    group_name = form.instance.group_name
    count = groups.filter(Q(code__exact=code) | Q(group_name__exact=group_name)).count()
    return count


def duplicate_restrictions(self, form):
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
    count = restrictions.filter(Q(code__exact=code) | Q(name__exact=name)).count()
    return count


def duplicate_roles(self, form):
    """
    If the role name already exists in the database, then return the count of the role name.

    :param form: The form instance that is being validated
    :return: The count of the number of roles that have the same name as the role being created or
    updated.
    """
    _id = self.kwargs.get("pk", None)
    roles = Roles.objects.all()

    if _id:
        roles = roles.exclude(id=_id)

    code = form.instance.code
    role_name = form.instance.role_name
    count = roles.filter(Q(code__exact=code) | Q(role_name__exact=role_name)).count()
    return count
