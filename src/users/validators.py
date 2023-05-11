from typing import List
from django.core.exceptions import ValidationError

# `docext` is a list that contains the allowed file extensions for a document. In this case, the
# allowed extensions are ".png", ".jpeg", ".jpg", and ".pdf". This list is used in the
# `validate_extension` function to check if a file has an allowed extension.
docext = [".pdf"]

imgext = [".png", ".jpeg", ".jpg", ".gif", ".heic", ".jfif"]


def validate_size(file, limit=2000000):
    """
    This function validates the size of a file and raises an error if it exceeds 2Mb.

    :param file: The "file" parameter is an object that represents a file that is being uploaded or
    processed in some way. The function "validate_size" takes this file object as input and checks its
    size. If the size is greater than 2Mb, it raises a validation error with a message indicating that
    the
    :return: the `file` object after validating its size.
    """
    size = file.size

    mb = limit / 1000000

    if size > limit:
        raise ValidationError(
            f"El archivo es demasiado pesado. Asegúrese de no subir archivos superiores a {mb}Mb"
        )

    return file


def validate_extension(file, fileext=imgext):
    """
    This function validates if a file has an allowed extension and raises a validation error if not.

    :param file: The file that needs to be validated for its extension
    :param fileext: The file extensions that are allowed for validation. It is a list of strings
    :return: the `file` object if its extension matches any of the extensions in the `fileext` list. If
    none of the extensions match, a `ValidationError` is raised with a message indicating the allowed
    file extensions.
    """

    for ext in fileext:
        if file.name.endswith(ext):
            return file

    error = "Archivos permitidos: " + "; ".join(fileext)
    raise ValidationError(error)


def validate_document(value):
    """
    The function "validate_document" takes a value, validates its size and extension, and returns the
    validated value.

    :param value: The input document that needs to be validated
    :return: The function `validate_document` is returning the validated `value` after it has been
    passed through the `validate_size` and `validate_extension` functions.
    """
    value = validate_size(value)
    value = validate_extension(value, fileext=docext)

    return value


def validate_image(value):
    """
    The function validates the size and extension of an image file.

    :param value: The input value to be validated, which is expected to be an image file
    :return: The function `validate_image` returns the validated `value` after passing it through the
    `validate_size` and `validate_extension` functions.
    """
    value = validate_size(value)
    value = validate_extension(value, fileext=imgext)

    return value
