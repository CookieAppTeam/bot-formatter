from .dpy import ConvertSetup
from .yml import remove_duplicate_new_lines
from .pycord import ConvertContext
from .lang import check_missing_keys, check_empty_line_diffs


EZCORD = [ConvertContext]
LANG = [check_missing_keys, check_empty_line_diffs]
PYCORD = []
DPY = [ConvertSetup]
YML = [remove_duplicate_new_lines]
