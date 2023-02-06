# EXTRA MODULES
import sweetify


def form_invalid_message(request):
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
