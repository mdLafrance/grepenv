"""Entrypoint logic for the module and cli command.
"""

import os
import sys
import typer

import pyperclip

from grepenv.cli import (
    print_path,
    highlight_string,
    print_environment,
    print_error,
    print_matching_keys,
    show_examples,
    try_compile_regex_pattern,
)

from .grepenv import filter_env_by_regular_expression, parse_environment


app = typer.Typer(add_completion=False)

_HELP_STRING = """
greps the env

\b
By default, all keys and values are searched for matches.
See options to specify only keys, or only values.

\b
Pattern matching is done using regex SEARCH. Use anchor characters if 
matching the whole key or value is necessary.
"""

_EPILOG_STRING = """
Call grepenv with the --example flag to see some example usage.
"""


@app.command(help=_HELP_STRING, epilog=_EPILOG_STRING)
def _(
    pattern: str = typer.Argument(
        None, help="Regular expression pattern to search with."
    ),
    path: bool = typer.Option(
        False, "-p", "--path", help="Search the PATH environment variable only"
    ),
    find_key: bool = typer.Option(
        False,
        "-fk",
        "--find-key",
        help="Modified behavior of grepenv. Will grep for all keys that match the given pattern, and return their corresponding value with no formatting, one per line.",
    ),
    case_sensitive: bool = typer.Option(
        False,
        "-cs",
        "--case-sensitive",
        help="Respect the case of pattern characters. By default, the given regular expression will be set to ignore the case of alphabetic characters.",
    ),
    keys_only: bool = typer.Option(False, "-k", "--keys", help="Only search keys."),
    values_only: bool = typer.Option(
        False, "-v", "--values", help="Only search values."
    ),
    no_highlight: bool = typer.Option(
        False, "-nh", "--no-highlight", help="Disable match highlighting."
    ),
    example: bool = typer.Option(False, "--example", help="Print some example usage."),
):
    # Exit on example
    if example:
        return show_examples()

    # Special case - if no pattern given, this means grep for everything
    # This also means, no highlight, since everything just gets highlighted
    if not pattern:
        pattern = ".*"
        no_highlight = True

    pat = try_compile_regex_pattern(pattern, ignore_case=not case_sensitive)

    if path:
        return print_path(pat, highlight=not no_highlight)

    # Handle find key branch
    if find_key:
        return print_matching_keys(parse_environment(), pat)

    # Regular highlight and print functionality
    env = filter_env_by_regular_expression(
        pat, keys_only=keys_only, values_only=values_only
    )

    print_environment(
        env,
        pat,
        keys_only=keys_only,
        values_only=values_only,
        highlight=not no_highlight,
    )


def main():
    app()


if __name__ == "__main__":
    main()
