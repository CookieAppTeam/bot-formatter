from .dpy import ConvertSetup
from .yml import remove_duplicate_new_lines
from .pycord import ConvertContext
from .lang_keys import check_missing_keys
from .lang_content import check_empty_line_diffs


EZCORD = [ConvertContext]
LANG_KEYS = [check_missing_keys]
LANG_CONTENT = [check_empty_line_diffs]
PYCORD = []
DPY = [ConvertSetup]
YML = [remove_duplicate_new_lines]
