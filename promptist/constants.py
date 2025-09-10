import re


RGX_PLACEHOLDER = re.compile(r"(?P<placeholder>{(?P<type>\w+):(?P<name>[\w.]+)})", re.IGNORECASE | re.MULTILINE)
RGX_CLEANER = re.compile(r"[^\w\s]", re.IGNORECASE | re.MULTILINE)

SUPPORTED_PLACEHOLDER_TYPES = {"data", "include"}


