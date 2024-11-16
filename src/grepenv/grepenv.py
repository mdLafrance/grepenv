"""Module grepenv provides functionality for greping through the environment.
"""
import re
import os

from typing import List

from dataclasses import dataclass


@dataclass
class EnvItem:
    """A single key/value pair entry in the environment."""

    key: str
    value: str


def parse_environment() -> List[EnvItem]:
    """Extract all key/value pairs from the environment."""
    env_items = [EnvItem(k, v) for k, v in os.environ.items()]
    return sorted(env_items, key=lambda e: e.key.lower())


def filter_env_by_regular_expression(
    pat: re.Pattern, keys_only: bool = False, values_only: bool = False
) -> List[EnvItem]:
    """Filters the environment for key/value pairs that match the given regular
    expression.
    """

    filter_fn = lambda e: (pat.search(e.key) and not values_only) or (
        pat.search(e.value) and not keys_only
    )

    return [e for e in parse_environment() if filter_fn(e)]


def highlight_string(var: str, pat: re.Pattern) -> str:
    """Scan the given string variable, and return a modified version in which
    all ranges matched by `pat` surrounded in `rich` highlighting tags.
    """
    if not pat.search(var):
        return var

    for m in reversed(list(pat.finditer(var))):
        start = m.start()
        end = m.end()

        s0 = var[:start]
        s1 = var[start:end]
        s2 = var[end:]

        var = rf"{s0}[red3]{s1}[/]{s2}"

    return var
