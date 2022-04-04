import fnmatch
import re


def is_a_match(pattern, name):
    return re.compile(fnmatch.translate(pattern)).match(name) is not None
