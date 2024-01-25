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

    assert filter_env_by_regular_expression(re.compile("v", re.I), values_only=True) == [
        EnvItem("PATH", "/a/b/c:/d/e/f/v"),
        EnvItem("VAL1", "VAL2"),
    ]

    assert filter_env_by_regular_expression(re.compile("v")) == [
        EnvItem("PATH", "/a/b/c:/d/e/f/v"),
    ]
