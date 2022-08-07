import ntpath
import os
import posixpath
from pathlib import PurePosixPath, PureWindowsPath

from colorama import Fore, Style


def styled_text(text, category, no_color):
    if no_color:
        return text

    mapping = {
        "major": Fore.RED,
        "minor": Fore.CYAN,
        "patch": Fore.GREEN,
        "other": Fore.MAGENTA,
        "info": Fore.BLUE,
        "cmd": Fore.YELLOW,
        "warning": Fore.YELLOW,
        "success": Fore.GREEN,
    }

    color = mapping.get(category)

    if color:
        return color + text + Style.RESET_ALL

    return text


# https://stackoverflow.com/a/72064941
def dot_path(pth):
    """Return path str that may start with '.' if relative."""
    if pth.is_absolute():
        return os.fsdecode(pth)
    if isinstance(pth, PureWindowsPath):
        return ntpath.join(".", pth)
    elif isinstance(pth, PurePosixPath):
        return posixpath.join(".", pth)
    else:
        return os.path.join(".", pth)
