import importlib
from pprint import pprint

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin
from django.urls import resolve


from .utils import verify_dispatch, validate_urlpattern


class UserLoggedMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("home_app:home_page"))
        return super().dispatch(request, *args, **kwargs)


class UserWithoutPermissions:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        This function checks if a user has permission to access a certain URL and redirects them if they
        don't.

        :param request: The HTTP request object that contains information about the incoming request,
        such as the URL, headers, and data
        :return: the response object that is obtained by calling the get_response() method with the
        request object passed as an argument. If certain conditions are met, the function may also
        return an HttpResponseRedirect object that redirects the user to the home page.
        """
        response = self.get_response(request)

        url_resolve = resolve(request.path_info)

        if not request.user.is_staff and url_resolve.url_name:
            try:
                urlpatterns = f"{url_resolve.app_names[0]}:{url_resolve.url_name}"
                dispatch = verify_dispatch(urlpatterns)
                if dispatch:
                    result = validate_urlpattern(request, urlpatterns)

                    candidature_save = None

                    if result:
                        candidature_save = result.filter(
                            name="offers_app:candidature_save"
                        )

                    if not candidature_save:
                        username = (
                            "username" in url_resolve.kwargs
                            and url_resolve.kwargs["username"]
                        )
                        slug = username
                        if not username:
                            slug = (
                                "slug" in url_resolve.kwargs
                                and url_resolve.kwargs["slug"]
                            )

                        if result and username:
                            if (
                                not username == request.user.username
                                and not slug == request.user.username
                            ):
                                result = 0

                        if not result:
                            return HttpResponseRedirect(
                                reverse_lazy("home_app:home_page")
                            )

            except Exception as ex:
                print(f"Error in UserWithoutPermissions: {ex}")

        return response
