from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin


class UserLoggedMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("home_app:home_page"))
        return super().dispatch(request, *args, **kwargs)
