import os
import sys
import traceback

import click

import wackywango


#imports to delete
from .utils import Connection
from .utils import Listener

class Log:

    def __init__(self):
        self.quiet = False
        self.traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info(): # there's an active exception
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


@main.group()
@click.pass_context
def client(context):
    context.obj['client'] = wackywango.Client()

@client.command('upload_thought')
@click.argument('address')
@click.argument('user', type=int)
@click.argument('thought')
@click.pass_obj
def client_upload_thought(obj, address, user, thought):
    client = obj['client']
    log(client.upload_thought(address, user, thought))



@main.command('read')
@click.argument('path')
def read_mind_data(path):
    reader = wackywango.Reader(path)
    for snapshot in reader:
        with Connection.connect(address='127.0.0.1', port=8000) as connection:
            connection.send_message('Hello, world!'.encode('utf-8')) # prepends size
        # log(snapshot)


@main.command('server')
def listen():
    while True:
        with Listener(port=8000) as listener:
            connection = listener.accept()
            print(connection.receive_message()) # prints 'Hello, world!'



if __name__ == '__main__':
    try:
        main(prog_name='wackywango', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
