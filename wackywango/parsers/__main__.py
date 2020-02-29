
import os
import sys
import traceback
import click

import wackywango.parsers


class Log:

    def __init__(self):
        self.quiet = False
        self.traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info():  # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)


log = Log()


@click.group()
@click.version_option(wackywango.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback


@main.command('parse')
@click.argument('parser_type')
@click.argument('data')
def parse(parser_type,data):
    log(wackywango.parsers.run_parser(parser_type,data))

if __name__ == '__main__':
    try:
        main(prog_name='wackywango', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
