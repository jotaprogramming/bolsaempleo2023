import importlib
from pprint import pprint

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin
from django.urls import resolve


from .utils import verify_dispatch


class UserLoggedMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("home_app:home_page"))
        return super().dispatch(request, *args, **kwargs)


class UserWithoutPermissions:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        url_resolve = resolve(request.path_info)
        
        if not request.user.is_staff and url_resolve.url_name:
            try:
                urlpatterns = f"{url_resolve.app_names[0]}:{url_resolve.url_name}"
                dispatch = verify_dispatch(urlpatterns)
                if dispatch:
                    rules = request.user.rule_user.all()
                    usergroups = [rule.usergroup for rule in rules]
                    roles = [rule.role for rule in rules]
                    policies = [
                        usergroup.usergroup_policy.all() for usergroup in usergroups
                    ]
                    
                    result = 0
                    # policy_apps = []
                    # policy_restrictions = []
                    for qs in policies:
                        for policy in qs:
                            # policy_restrictions.append(policy.restriction.all())
                            # policy_apps.append(policy.app.all())
                            result = policy.app.all().filter(name=urlpatterns)

                            # if result.count():
                            #     return response
                            # for app in policy.app.all():
                            #     print(
                            #         "🐍 File: core/middlewares.py | Line: 46 | __call__ ~ app",
                            #         app.route,
                            #     )

                    username = url_resolve.kwargs["username"]
                    if result and username and not username == request.user.username:
                        result = 0

                    if not result:
                        return HttpResponseRedirect(
                            reverse_lazy("home_app:home_page")
                        )

            except Exception as ex:
                print(f"Error: {ex}")

        return response
