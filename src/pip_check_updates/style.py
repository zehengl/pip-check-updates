import ntpath
import os
import posixpath
from pathlib import PurePosixPath, PureWindowsPath


def styled_text(text, category, no_color):
    if no_color:
        return text

    mapping = {
        "major": "red",
        "minor": "cyan",
        "patch": "green",
        "other": "magenta",
        "info": "blue",
        "cmd": "yellow",
        "warning": "bold yellow",
        "success": "bold green",
        "error": "bold red",
        "version": "bold italic",
    }

    style = mapping.get(category)

    if style:
        return f"[{style}]{text}[/{style}]"

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
