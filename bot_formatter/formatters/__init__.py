from .dpy import ConvertSetup
from .lang import check_empty_line_diffs, check_missing_keys
from .pycord import ConvertContext
from .yml import remove_duplicate_new_lines

EZCORD = [ConvertContext]
LANG = [check_missing_keys, check_empty_line_diffs]
PYCORD: list = []
DPY = [ConvertSetup]
YML = [remove_duplicate_new_lines]
