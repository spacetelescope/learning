from json import load

from server import es, ix, get_results


def main():
    for doc in load(open('helps.json')).values():
        es.index(index=ix, id=doc['title'], body=doc)
    es.indices.refresh(index=ix)


if __name__ == '__main__':
    main()
    get_results('Outlook Calendar app', 5)
