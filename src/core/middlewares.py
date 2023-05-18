import importlib
from pprint import pprint

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin
from django.urls import resolve
from django.db.models import Q, F, Count, Sum, Case, When, BooleanField, IntegerField


from .utils import verify_dispatch, validate_permissions


class UserLoggedMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        """
        This function checks if the user is authenticated and redirects them to the home page if they
        are, otherwise it calls the parent dispatch method.
        
        :param request: The HTTP request object that contains information about the incoming request,
        such as the request method, headers, and body
        :return: If the user is authenticated, a redirect response to the home page is being returned.
        Otherwise, the dispatch method of the parent class is being called with the request, *args, and
        **kwargs arguments and its response is being returned.
        """
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("home_app:home_page"))
        return super().dispatch(request, *args, **kwargs)


class UserWithoutPermissions:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        This function checks if a user has the necessary permissions to access a certain URL and
        redirects them to the home page if they do not.
        
        :param request: The HTTP request object that contains information about the incoming request,
        such as the URL, headers, and data
        :return: the `response` object that is obtained by calling `self.get_response(request)`.
        """
        response = self.get_response(request)

        url_resolve = resolve(request.path_info)

        if not request.user.is_staff and url_resolve.url_name:
            try:
                urlpatterns = f"{url_resolve.app_names[0]}:{url_resolve.url_name}"
                dispatch = verify_dispatch(urlpatterns)
                if dispatch:
                    restrictions = validate_permissions(request, urlpatterns)

                    if not restrictions:
                        return HttpResponseRedirect(reverse_lazy("home_app:home_page"))

            except Exception as ex:
                print(f"Error in UserWithoutPermissions: {ex}")

        return response
