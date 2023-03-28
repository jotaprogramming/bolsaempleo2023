import base64
import sys, codecs


def string_to_base64(sample_string):
    sample_string_bytes = sample_string.encode("ascii")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string


def base64_to_string(base64_string):
    if '===' in base64_string:
        return ""
    try:
        base64_bytes = base64_string.encode("ascii")

        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        return sample_string
    except:
        base64_to_string(f'{base64_string}=')
