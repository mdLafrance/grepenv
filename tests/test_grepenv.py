"""Unit tests for grepenv module
"""
import re
import os

from unittest import mock

from grepenv.grepenv import EnvItem, parse_environment, filter_env_by_regular_expression


@mock.patch.dict(
    os.environ, {"VAL1": "VAL2", "test": "asdf", "PATH": "/a/b/c:/d/e/f"}, clear=True
)
def test_parse_environment():
    assert parse_environment() == [
        EnvItem("PATH", "/a/b/c:/d/e/f"),
        EnvItem("test", "asdf"),
        EnvItem("VAL1", "VAL2"),
    ]


@mock.patch.dict(
    os.environ, {"VAL1": "VAL2", "test": "asdf", "PATH": "/a/b/c:/d/e/f/v"}, clear=True
)
def test_filter_env_by_regular_expression():
    assert filter_env_by_regular_expression(re.compile("v", re.I)) == [
        EnvItem("PATH", "/a/b/c:/d/e/f/v"),
        EnvItem("VAL1", "VAL2"),
    ]

    assert filter_env_by_regular_expression(re.compile("a.*f", re.I)) == [
        EnvItem("PATH", "/a/b/c:/d/e/f/v"),
        EnvItem("test", "asdf"),
    ]

    assert filter_env_by_regular_expression(re.compile("v", re.I), keys_only=True) == [
        EnvItem("VAL1", "VAL2"),
    ]

    assert filter_env_by_regular_expression(
        re.compile("v", re.I), values_only=True
    ) == [
        EnvItem("PATH", "/a/b/c:/d/e/f/v"),
        EnvItem("VAL1", "VAL2"),
    ]

    assert filter_env_by_regular_expression(re.compile("v")) == [
        EnvItem("PATH", "/a/b/c:/d/e/f/v"),
    ]


def test_highlight_string():
    from grepenv.grepenv import highlight_string

    expected = (
        (
            "go",
            "/usr/bin/go:/usr/env/asdf:/foo/golang/bar",
            "/usr/bin/[red3]go[/]:/usr/env/asdf:/foo/[red3]go[/]lang/bar",
        ),
        (
            "10",
            "SOME_VAR=ANOTHER_VAR",
            "SOME_VAR=ANOTHER_VAR",
        ),
        ("a", "a", "[red3]a[/]"),
    )

    for pat, before, expected in expected:
        res = highlight_string(before, re.compile(pat))

        assert res == expected
