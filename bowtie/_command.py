# -*- coding: utf-8 -*-
"""
Decorates a function for Bowtie.

Reference
---------
https://gist.github.com/carlsmith/800cbe3e11f630ac8aa0
"""

import sys
import inspect
from subprocess import call

import click


def command(func):
    """
    Decorates a function for building a Bowtie
    application and turns it into a command line interface.

    """

    @click.group(options_metavar='[-p <path>] [--help]')
    @click.option('--path', '-p', default='build', type=str,
                  help='Path to build the app.')
    @click.pass_context
    def cmd(ctx, path):
        """
        Bowtie CLI to help build and run your app.
        """
        ctx.obj = path

    # pylint: disable=unused-variable
    @cmd.command()
    @click.pass_context
    def build(ctx):
        """
        Writes the app, downloads the packages, and bundles it with Webpack.
        """
        try:
            func(ctx.obj)
        except TypeError:
            func()

    @cmd.command(context_settings=dict(ignore_unknown_options=True))
    @click.argument('extra', nargs=-1, type=click.UNPROCESSED)
    @click.pass_context
    def serve(ctx, extra):
        """
        Serves the Bowtie app locally.
        """
        line = ('./{}/src/server.py'.format(ctx.obj),) + extra
        call(line)

    @cmd.command(context_settings=dict(ignore_unknown_options=True))
    @click.argument('extra', nargs=-1, type=click.UNPROCESSED)
    @click.pass_context
    def dev(ctx, extra):
        """
        Recompiles the app for development.
        """
        line = ('webpack', '-d') + extra
        call(line, cwd=ctx.obj)

    @cmd.command(context_settings=dict(ignore_unknown_options=True))
    @click.argument('extra', nargs=-1, type=click.UNPROCESSED)
    @click.pass_context
    def prod(ctx, extra):
        """
        Recompiles the app for production.
        """
        line = ('webpack', '-p') + extra
        call(line, cwd=ctx.obj)

    locale = inspect.stack()[1][0].f_locals
    module = locale.get("__name__", None)

    if module == "__main__":
        try:
            arg = sys.argv[1:]
        except IndexError:
            arg = '--help',
        # pylint: disable=no-value-for-parameter
        sys.exit(cmd(arg))

    return cmd