import typer

from grepenv.cli import highlight_string, print_environment, try_compile_regex_pattern

from .grepenv import filter_env_by_regular_expression, modify_pattern_to_ignore_case

from rich import print

app = typer.Typer(add_completion=False, no_args_is_help=True)

_HELP_STRING = """
greps the env

\b
By default, all keys and values are searched for matches.
See options to specify only keys, or only values.
"""


@app.command(
    help=_HELP_STRING,
)
def _(
    pattern: str = typer.Argument(
        ..., help="Regular expression pattern to search with."
    ),
    respect_case: bool = typer.Option(False, "-c", "--respect-case", help="Respect case of pattern characters."),
    keys_only: bool = typer.Option(False, "-k", "--keys", help="Only search keys."),
    values_only: bool = typer.Option(
        False, "-v", "--values", help="Only search values."
    ),
    no_highlight: bool = typer.Option(
        False, "-nh", "--no-highlight", help="Disable match highlighting."
    ),
):
    # Filter environment variables
    pat = try_compile_regex_pattern(pattern, ignore_case = not respect_case)
    env = filter_env_by_regular_expression(
        pat, keys_only=keys_only, values_only=values_only
    )

    print_environment(env, pat, keys_only=keys_only, values_only=values_only, highlight=not no_highlight)


def main():
    app()


if __name__ == "__main__":
    main()
