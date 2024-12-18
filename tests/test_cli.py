"""Unit tests for cli.py module
"""
import re

import pytest

from grepenv.cli import format_environment_item, highlight_string
from grepenv.grepenv import EnvItem

from unittest.mock import patch


def test_try_compile_regex_pattern():
    import re
    from grepenv.cli import try_compile_regex_pattern

    correct_patterns = (
        "asdf",
        r"(\W|^)[\w.\-]{0,25}@(yahoo|hotmail|gmail)\.com(\W|$)",
        ".*",
    )

    incorrect_patterns = ("[", "*", "adsfjaj)")

    for p in correct_patterns:
        assert re.compile(p) is not None

    for p in incorrect_patterns:
        with pytest.raises(SystemExit) as exit:
            try_compile_regex_pattern(p)

        assert exit.type == SystemExit
        assert exit.value.code == 1


def test_format_environment_item():
    i = EnvItem("TEST_KEY", "TEST_VALUE")

    assert (
        format_environment_item(i, re.compile("TEST"))
        == "[red3]TEST[/]_KEY=[red3]TEST[/]_VALUE"
    )

    assert (
        format_environment_item(i, re.compile("TEST"), keys_only=True)
        == "[red3]TEST[/]_KEY=[dim]TEST_VALUE[/]"
    )

    assert (
        format_environment_item(i, re.compile("TEST"), values_only=True)
        == "[dim]TEST_KEY[/]=[red3]TEST[/]_VALUE"
    )

    assert (
        format_environment_item(
            i, re.compile("TEST"), values_only=True, highlight=False
        )
        == "TEST_KEY=TEST_VALUE"
    )

    assert (
        format_environment_item(i, re.compile("KEY"), values_only=True)
        == "[dim]TEST_KEY[/]=TEST_VALUE"
    )

    assert (
        format_environment_item(i, re.compile("KEY")) == "TEST_[red3]KEY[/]=TEST_VALUE"
    )


def test_print_path():
    from grepenv.cli import print_path

    # Test we panic if there's no path
    with patch("os.environ", {}):
        with pytest.raises(SystemExit):
            print_path(re.compile(".*"), True)
