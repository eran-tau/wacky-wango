import os
import sys
import traceback
import click

import wackywango.cli


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
@click.option('--host', '-h',
              default="127.0.0.1",
              show_default='127.0.0.1')
@click.option('--port', '-p',
              default="5000",
              show_default='5000')
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
@click.pass_context
def main(context, host, port, quiet=False, traceback=False):
    context.obj['cli'] = wackywango.cli.CLI(host,port)
    log.quiet = quiet
    log.traceback = traceback


@main.command('get-users')
@click.pass_obj
def get_users(obj):
    log(obj['cli'].get_users())

@main.command('get-user')
@click.argument('user_id')
@click.pass_obj
def get_user(obj,user_id):
    log(obj['cli'].get_user(user_id))

@main.command('get-snapshots')
@click.argument('user_id')
@click.pass_obj
def get_snapshots(obj,user_id):
    log(obj['cli'].get_snapshots(user_id))

@main.command('get-snapshot')
@click.argument('user_id')
@click.argument('snapshot_id')
@click.pass_obj
def get_snapshot(obj,user_id,snapshot_id):
    log(obj['cli'].get_snapshot(user_id,snapshot_id))

@main.command('get-result')
@click.argument('user_id')
@click.argument('snapshot_id')
@click.argument('parser_type')
@click.option('--save', '-s')
@click.pass_obj
def get_result(obj,user_id,snapshot_id,parser_type,save):
    if save:
        log(obj['cli'].get_result_and_save(user_id,snapshot_id,parser_type,save))
    else:
        log(obj['cli'].get_result(user_id, snapshot_id, parser_type))


if __name__ == '__main__':
    try:
        main(prog_name='wackywango', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
