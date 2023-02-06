# PROJECT MODULES
from users.models import *
from core.utils import *
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


def diplicate_usergroups(self, form):
    _id = self.kwargs.get("pk", None)
    groups = UserGroups.objects.all()

    if _id:
        groups = groups.exclude(id=_id)

    group_name = form.instance.group_name
    count = groups.filter(group_name__exact=group_name).count()
    return count

def diplicate_restrictions(self, form):
    _id = self.kwargs.get("pk", None)
    restrictions = Restrictions.objects.all()

    if _id:
        restrictions = restrictions.exclude(id=_id)

    code = form.instance.code
    name = form.instance.name
    count_code = restrictions.filter(code__exact=code).count()
    count_name = restrictions.filter(name__exact=name).count()
    return count_code, count_name
