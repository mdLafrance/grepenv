import re
import os

from typing import List

from pathlib import Path

from dataclasses import dataclass


@dataclass
class EnvItem:
    """A single key/value pair entry in the environment."""

    key: str
    value: str


def modify_pattern_to_ignore_case(pattern: str) -> str:
    modified = ""

    for c in pattern:
        if str(c).isalpha():
            modified += f"[{c}{c.upper()}]"
        else:
            modified += c

    return modified


def parse_environment() -> List[EnvItem]:
    """Extract all key/value pairs from the environment."""
    return [EnvItem(k, v) for k, v in os.environ.items()]


def filter_env_by_regular_expression(
    pat: re.Pattern, keys_only: bool = False, values_only: bool = False
) -> List[EnvItem]:
    """Filters the environment for key/value pairs that match the given regular
    expression.
    """

    filter_fn = lambda e: (pat.search(e.key) and not values_only) or (pat.search(e.value) and not keys_only)

    return [e for e in parse_environment() if filter_fn(e)]
