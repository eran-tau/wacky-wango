import os
import sys
import traceback
import click

import wackywango.gui


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


@main.command('run-server')
@click.option('--host', '-h',
              default="127.0.0.1",
              show_default='127.0.0.1')
@click.option('--port', '-p',
              default="8080",
              show_default='8080')
@click.option('--api-host', '-H',
              default="127.0.0.1",
              show_default='127.0.0.1')
@click.option('--api-port', '-P',
              default="5000",
              show_default='5000')
def run_server(host, port, api_host, api_port):
    log(wackywango.gui.run_server(host, port, api_host, api_port))


if __name__ == '__main__':
    try:
        main(prog_name='wackywango', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
