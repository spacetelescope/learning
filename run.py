from importlib import import_module
from pprint import pprint

from ipdb import launch_ipdb_on_exception
import click

from corpus import get_messages


def main():
    # pprint(list(get_users()))
    pprint(list(get_messages(100)))


@click.command()
@click.option('-i', '--ipdb', is_flag=True, help='Drop into ipdb on errors')
@click.argument('module')
def cmd(ipdb, module):
    modmain = getattr(import_module(module), 'main', main)
    if ipdb:
        with launch_ipdb_on_exception():
            modmain()
    else:
        modmain()


if __name__ == "__main__":
    cmd()
