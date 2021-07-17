from importlib import import_module
from pprint import pprint
from contextlib import contextmanager
from time import time

from ipdb import launch_ipdb_on_exception
import click

from corpus import get_messages


@contextmanager
def nullcontext(enter_result=None):
    yield enter_result


def main():
    # pprint(list(get_users()))
    print(len(list(get_messages(verbosity=0))))


@click.command()
@click.option('-i', '--ipdb', is_flag=True, help='Drop into ipdb on errors')
@click.argument('modules', nargs=-1)
def cmd(ipdb, modules):
    ctx = launch_ipdb_on_exception if ipdb else nullcontext
    if not modules:
        with ctx():
            main()
        return
    for module in modules:
        with ctx():
            getattr(import_module(module), 'main', main)()


if __name__ == "__main__":
    cmd()
