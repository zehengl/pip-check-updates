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
