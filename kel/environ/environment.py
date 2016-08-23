import os

from .exceptions import ImproperlyConfigured


def env(key, kind="str", default=""):
    if callable(default):
        default = default()
    value = os.environ.get(key, default)
    if kind == "bool":
        value = parse_bool(value)
    elif kind == "int":
        value = parse_int(value)
    elif kind == "list":
        value = parse_list(value)
    elif kind == "str":
        pass
    elif callable(kind):
        value = kind(value)
    else:
        raise ValueError('"{}" is not a valid environment variable value (must be predefined or a callback)'.format(kind))
    return value


def parse_bool(value):
    v = {
        # True mappings
        "1": True,
        "t": True,
        "T": True,
        "TRUE": True,
        "true": True,
        "True": True,
        True: True,
        # False mappings
        "0": False,
        "f": False,
        "F": False,
        "FALSE": False,
        "false": False,
        "False": False,
        False: False,
    }.get(value)
    if v is None:
        raise ImproperlyConfigured('"{}" is not a valid boolean value'.format(value))
    return v


def parse_int(value):
    try:
        return int(value)
    except ValueError:
        raise ImproperlyConfigured('"{}" is not a valid integer value'.format(value))


def parse_list(value, cast=str):
    if isinstance(value, str):
        value = map(cast, value.split(","))
    return list(value)
