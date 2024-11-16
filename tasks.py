"""Command line runnable task definitions for use with pyinvoke.
"""
from invoke import task

@task
def lint(c):
    c.run("poetry run black ./src")


@task
def test(c):
    c.run("poetry run coverage run -m pytest tests/")
    c.run("poetry run coverage report --omit=\"tests/*\" --fail-under=75 --show-missing")


@task
def build(c):
    c.run("poetry build")

@task
def publish(c):
    c.run("poetry publish")
