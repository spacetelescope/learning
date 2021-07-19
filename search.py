from json import load
from pprint import pprint
from flask import Flask, jsonify, request

from elasticsearch import Elasticsearch

es = Elasticsearch()

# from whoosh.qparser import MultifieldParser
# from whoosh import index
# from whoosh.fields import ID, TEXT, Schema
#
# schema = Schema(title=TEXT(stored=True), url=ID(stored=True), content=TEXT(stored=True))
app = Flask('search')


def content():
    ix = index.create_in('indexdir', schema)
    writer = ix.writer()
    for doc in load(open('blogs/content.json')).values():
        writer.add_document(**doc)
    writer.commit()
    return ix


def read():
    return index.open_dir('indexdir')


# ix = read()
ix = "slack-help"


def helper():
    for doc in load(open('help/helps.json')).values():
        es.index(index=ix, id=doc['title'], body=doc)
    es.indices.refresh(index=ix)


helper()


def mkquery(q, n):
    return {
        'from': 0,
        'size': n,
        'query': {
            'fuzzy': {
                'content': {
                    'value': q
                }
            }
        }
    }


def get_whoosh_results(q, n):
    with ix.searcher() as searcher:
        query = MultifieldParser(['title', 'content', 'url'], ix.schema).parse(q)
        results = {'response': [dict(result) for result in searcher.search(query)][:n]}
    return results


def get_es_results(q, n):
    res = es.search(index=ix, body=mkquery(q, n))
    print("Got %d Hits:" % res['hits']['total']['value'])
    total = []
    for hit in res['hits']['hits']:
        hs = hit['_source']
        print(f"{hs['title']}: {hs['content']}"[:100])
        total.append({'url': hs['url'], 'title': hs['title'], 'content': hs['content']})
    return total


# pprint(get_es_results('emoji', 10))


@app.route('/', methods=['GET', 'POST'])
def search():
    q = request.form.get('q', '')
    n = int(request.form.get('n', '5'))
    # q = 'document'
    print(request.form)

    # return jsonify(get_whoosh_results(q, n))
    return jsonify(get_es_results(q, n))
