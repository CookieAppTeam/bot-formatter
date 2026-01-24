from .dpy import ConvertSetup
from .ezcord import ConvertContext
from .lang import (
    check_empty_line_diffs,
    check_key_order,
    check_missing_keys,
    check_variables,
)
from .yml import remove_duplicate_new_lines

PYCORD: list = []
DPY = [ConvertSetup]
EZCORD = [ConvertContext]

LANG = [check_missing_keys, check_key_order, check_empty_line_diffs, check_variables]
YML = [remove_duplicate_new_lines]
