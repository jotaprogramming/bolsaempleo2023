import base64
import sys, codecs


POST_STATUS = (
    ("1", "aplicado"),
    ("2", "cancelado"),
    ("3", "rechazado"),
    ("4", "aceptado"),
    ("5", "contratado"),
)


def string_to_base64(sample_string):
    sample_string_bytes = sample_string.encode("ascii")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string


def base64_to_string(base64_string):
    if "===" in base64_string:
        return ""
    try:
        base64_bytes = base64_string.encode("ascii")

        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        return sample_string
    except:
        base64_to_string(f"{base64_string}=")


def get_pk_from_a_slug(self):
    slug = self.kwargs.get("slug", "")
    slug_split = slug.split("-")
    split_pk = slug_split[-1]
    # str_pk = base64_to_string(f"{split_pk}")
    return split_pk


def get_status_name(p_stauts):
    for status in POST_STATUS:
        _id = status[0]
        if _id == p_stauts:
            return status[1]
