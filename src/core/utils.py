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


def error_message(request, msg=_("An unexpected error occurred")):
    """
    It takes a request object and a message, and then displays a sweetalert2 popup with the message
    
    :param request: The request object
    :param msg: The message to display
    """
    swal_title = _("Error")
    swal_msg = msg
    swal_time = 5000
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
