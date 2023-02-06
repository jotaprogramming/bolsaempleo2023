# PYTHON MODULES
import importlib

# EXTRA MODULES
import sweetify
from pprint import pprint


def form_invalid_message(request):
    """
    It's a function that displays a message in the browser when a form is invalid.
    
    :param request: The request object
    """
    swal_title = "Advertencia"
    swal_msg = "Formulario inválido"
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


def created_message(request):
    """
    It creates a message that will be displayed to the user after a successful action.
    
    :param request: The request object
    """
    swal_title = "Éxito"
    swal_msg = "Registro creado satisfactoriamente"
    swal_time = 5000
    sweetify.success(
        request,
        title=swal_title,
        text=swal_msg,
        icon="success",
        timer=swal_time,
        timerProgressBar="true",
        button="Ok",
    )


def updated_message(request):
    """
    It's a function that takes a request as an argument and returns a sweetify success message
    
    :param request: The request object
    """
    swal_title = "Éxito"
    swal_msg = "Registro actualizado satisfactoriamente"
    swal_time = 5000
    sweetify.success(
        request,
        title=swal_title,
        text=swal_msg,
        icon="success",
        timer=swal_time,
        timerProgressBar="true",
        button="Ok",
    )


def deleted_message(request):
    """
    It's a function that takes a request as an argument and returns a sweetalert2 message
    
    :param request: The request object
    """
    swal_title = "Éxito"
    swal_msg = "Registro eliminado satisfactoriamente"
    swal_time = 5000
    sweetify.success(
        request,
        title=swal_title,
        text=swal_msg,
        icon="success",
        timer=swal_time,
        timerProgressBar="true",
        button="Ok",
    )


def duplicate_message(request):
    """
    It's a function that takes a request object and returns a sweetify warning message
    
    :param request: The request object
    """
    swal_title = "Advertencia"
    swal_msg = "El registro ya existe"
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


def error_message(request):
    """
    It takes a request object and displays a sweetalert2 error message.
    
    :param request: The request object
    """
    swal_title = "Error"
    swal_msg = "Ocurrió un error inesperado"
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
