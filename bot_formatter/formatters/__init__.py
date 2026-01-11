from .dpy import ConvertSetup
from .ezcord import ConvertContext
from .lang import check_empty_line_diffs, check_missing_keys
from .yml import remove_duplicate_new_lines

PYCORD: list = []
DPY = [ConvertSetup]
EZCORD = [ConvertContext]

LANG = [check_missing_keys, check_empty_line_diffs]
YML = [remove_duplicate_new_lines]
