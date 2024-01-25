"""Helper functionality for the cli.

These functions may call sys.exit(), and so should only be called form the
cli itself.
"""
import re
import sys

from typing import NoReturn, Union, List

from rich.console import Console

from grepenv.grepenv import EnvItem


_CONSOLE = Console()


def try_compile_regex_pattern(pattern: str, ignore_case: bool = True) -> Union[re.Pattern, NoReturn]:
    try:
        return re.compile(pattern, re.IGNORECASE if ignore_case else 0)
    except Exception as e:
        print_error(f"Couldn't compile regular expression ({e})")
        sys.exit(1)


def highlight_string(var: str, pat: re.Pattern) -> str:
    """Scan the given string variable, and return a modified version in which
    the range which matches `pat` is highlighted using rich.

    This doesn't print the variable.
    """
    if not pat.search(var):
        return var

    for m in reversed(list(pat.finditer(var))):
        start = m.start()
        end = m.end()

        # Modify string
        s0 = var[:start]
        s1 = var[start:end]
        s2 = var[end:]

        var = f"{s0}[red]{s1}[/]{s2}"

    return var


def print_environment(
    env: List[EnvItem],
    pat: re.Pattern,
    keys_only: bool = False,
    values_only: bool = False,
    highlight: bool = True,
):
    for x in env:
        # Format key
        if values_only:
            key_s = f"[dim]{x.key}[/]"
        elif highlight:
            key_s = highlight_string(x.key, pat)
        else:
            key_s = x.key

        # Format value
        if keys_only:
            value_s = f"[dim]{x.value}[/]"
        elif highlight:
            value_s = highlight_string(x.value, pat)
        else:
            value_s = x.value

        # concat
        _CONSOLE.print(f"{key_s}={value_s}", highlight=False)


def print_error(m: str):
    """Print a formatted error message `m`."""
    _CONSOLE.print(f"[bold error]ERROR: [/]{m}")
