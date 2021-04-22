from corpus import get_users, get_messages
from pprint import pprint
from ipdb import launch_ipdb_on_exception


def main():
    # pprint(list(get_users()))
    pprint(list(get_messages(100)))


if __name__ == "__main__":
    with launch_ipdb_on_exception():
        main()
