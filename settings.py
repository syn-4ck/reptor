import pathlib
from collections import OrderedDict
from classes.ToolBase import ToolBase
from classes.ConfBase import ConfBase
from classes.UploadBase import UploadBase

BASE_DIR = pathlib.Path(__file__).parent

MODULE_DIRS = BASE_DIR / "modules"

NEWLINE = '\n'

USER_AGENT = 'reptor CLI v0.0.1'  # TODO dynamic version

SUBCOMMANDS_GROUPS = OrderedDict({
    ConfBase: ('configuration', list()),
    UploadBase: ('upload', list()),
    ToolBase: ('tool output processing', list()),
    'other': ('other', list()),
})