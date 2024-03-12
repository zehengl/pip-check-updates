from importlib.metadata import version

try:
    __version__ = version("pip-check-updates")
except:
    __version__ = "0.0.0"
