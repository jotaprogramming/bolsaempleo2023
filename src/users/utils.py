# PROJECT MODULES
from users.models import *
from core.utils import *
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.decorators.debug import sensitive_variables


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


# def duplicate_apps(self, form):
#     """
#     It returns the number of apps that have the same name and route as the app being created or updated.

#     :param form: The form instance that was submitted
#     :return: A tuple of two integers.
#     """
#     _id = self.kwargs.get("pk", None)
#     apps = Apps.objects.all()

#     if _id:
#         apps = apps.exclude(id=_id)

#     name = form.instance.name
#     route = form.instance.route
#     count_name = apps.filter(name__exact=name).count()
#     count_route = apps.filter(route__exact=route).count()
#     return count_name, count_route


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


# def duplicate_traits(self, form):
#     _id = self.kwargs.get("pk", None)
#     traits = Traits.objects.all()

#     if _id:
#         traits = traits.exclude(id=_id)

#     user = form.instance.user
#     print("user: ", user)
#     print("instances: ", form)
#     app = form.instance.app
#     restriction = form.instance.restriction
#     role = form.instance.role
#     print(app, restriction, role)
#     count = traits.filter(
#         user__exact=user,
#         app__in=[app],
#         restriction__in=[restriction],
#         role__in=[role],
#     ).count()
#     return count


# def duplicate_users(self, form):
#     """
#     If the role name already exists in the database, then return the count of the role name.

#     :param form: The form instance that is being validated
#     :return: The count of the number of roles that have the same name as the role being created or
#     updated.
#     """
#     _id = self.kwargs.get("pk", None)
#     user = User.objects.all()

#     if _id:
#         user = user.exclude(id=_id)

#     username = form.instance.username
#     count = user.filter(username__exact=username).count()
#     return count
