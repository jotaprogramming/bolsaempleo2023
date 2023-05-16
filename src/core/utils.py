# DJANGO MODULES
from django import forms
from django.utils.translation import gettext as _

# PYTHON MODULES
import importlib
import json

# EXTRA MODULES
import sweetify
from pprint import pprint


def success_message(request, msg=_("Successfully created"), time=5000):
    """
    It creates a success message with a title, message, icon, timer, and button.

    :param request: The request object
    :param msg: The message to be displayed
    """
    swal_title = _("Success")
    swal_msg = msg
    swal_time = time
    sweetify.success(
        request,
        title=swal_title,
        text=swal_msg,
        icon="success",
        timer=swal_time,
        timerProgressBar="true",
        button="Ok",
    )


def warning_message(request, msg=_("Warning")):
    """
    It's a function that takes a request and a message as parameters and displays a warning message
    using sweetify.

    :param request: The request object
    :param msg: The message to be displayed
    """
    swal_title = _("Warning")
    swal_msg = msg
    swal_time = 5000
    sweetify.warning(
        request,
        title=swal_title,
        text=swal_msg,
        icon="warning",
        timer=swal_time,
        timerProgressBar="true",
        button="Ok",
    )


def error_message(request, msg=_("An unexpected error occurred"), time=5000):
    """
    It takes a request object and a message, and then displays a sweetalert2 popup with the message

    :param request: The request object
    :param msg: The message to display
    """
    swal_title = _("Error")
    swal_msg = msg
    swal_time = time
    sweetify.error(
        request,
        title=swal_title,
        text=swal_msg,
        icon="error",
        timer=swal_time,
        timerProgressBar="true",
        button="Ok",
    )


def get_form_errors(form):
    """
    It takes a Django form object and returns a string of all the errors in the form.

    :param form: The form object
    :return: A string with all the errors in the form.
    """
    json_errors = form.errors.as_json()
    errors = json.loads(json_errors)
    try:
        all_error = errors["__all__"][0]
    except:
        all_error = errors

    msg_error = ""

    if len(all_error.keys()) > 0:
        for key, value in all_error.items():
            for msg in value:
                msg_error += f"{msg['message']};\n"

    return msg_error


def normalize_email(email):
    """
    It normalizes the email address.

    :param email: The email address to be normalized
    :return: A string
    """
    _email = str(email).lower()
    verify_email = forms.EmailField()
    verify_email.clean(_email)
    return _email


def get_request_body(request):
    body_unicode = request.body.decode("utf-8")
    body_data = json.loads(body_unicode)

    return body_data


def set_data_status(data=[], status="204"):
    _type = "warning"
    msg = "No se encontraron registros"
    if int(status) >= 400:
        _type = "error"
        msg = _(
            "Ha ocurrido un error. Por favor inténtelo de nuevo o comuníquese con nuestro equipo de soporte"
        )
    elif data:
        status = "200"
        _type = "success"
        msg = ""
    return {"status": status, "type": _type, "msg": msg, "data": data}


def verify_dispatch(urlpatterns):
    """
    This function verifies if a given URL pattern in a Django app requires authentication.

    :param urlpatterns: The `urlpatterns` parameter is expected to be a string representing a URL
    pattern in the format `app_name:url_name`. For example, `myapp:home` would represent the URL pattern
    for the `home` view in the `myapp` Django application
    :return: a boolean value. It returns True if the given urlpatterns contain a URL pattern that has a
    view function with an inheritance from the Django authentication mixin, and False otherwise.
    """
    app_name, url_name = urlpatterns.split(":")
    app_module = importlib.import_module(app_name.replace("_app", ""))
    urls = getattr(app_module, "urlpatterns", [])

    for url in urls:
        if url.name == url_name:
            view_func = url.callback.view_class
            inheritances = view_func.mro()
            for inheritance in inheritances:
                if inheritance.__module__ == "django.contrib.auth.mixins":
                    return True

    return False


def validate_urlpattern(request, urlpatterns):
    """
    This function validates a URL pattern based on user rules, user groups, roles, and policies.

    :param request: The request object contains information about the current HTTP request, such as the
    user making the request, the HTTP method used, and any data submitted in the request
    :param urlpatterns: The `urlpatterns` parameter is a string representing a URL pattern that needs to
    be validated
    :return: True if the user has permission to access the provided URL pattern, False otherwise.
    """

    rules = request.user.rule_user.select_related("usergroup__usergroup_policy__app")
    for rule in rules:
        if rule.usergroup.usergroup_policy.filter(
            app__name__icontains=urlpatterns.strip()
        ).exists():
            return True

    return False
