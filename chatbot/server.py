from json import load
from os import getenv
from json import loads
from flask import Flask, jsonify, request, abort

from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from elasticsearch_dsl import Search

es = Elasticsearch(getenv('ES_HOSTS', 'localhost').split(','))
ix = 'chatbot'
app = Flask(__name__)


def helper():
    for doc in load(open('helps.json')).values():
        es.index(index=ix, id=doc['title'], body=doc)
    es.indices.refresh(index=ix)


def get_results(query, num):
    search = Search(using=es, index=ix).query("multi_match", query=query, fields=['title', 'content'])
    total = []
    for hit in search.execute():
        print(f"{hit.meta.score}={hit.title}: {hit.content}"[:140])
        total.append({'url': hit.url, 'title': hit.title, 'content': hit.content})
        if num and len(total) == num:
            return total
    return total


@app.route('/search', methods=['POST'])
def search():
    """
    Searches the ES index for articles matching the `q` query parameter text
    Limits the results to `n` articles
    """
    query = request.form.get('q', '')
    num = int(request.form.get('n', '5'))
    print(f'Query: {query} Limit: {num}')
    return jsonify({'response': get_results(query, num)})


@app.route('/index', methods=['POST'])
def index():
    try:
        data = loads(request.data)
    except ValueError:
        return 'No JSON data posted', 400
    if isinstance(data, dict):
        try:
            es.index(index=ix, id=data['id'], body=data)
        except KeyError:
            return 'Docs must have an id field', 400
    else:
        actions = []
        for action in data:
            action['_index'] = ix
            action['_id'] = action.pop('id')
            actions.append(action)
        streaming_bulk(es, actions)
    es.indices.refresh(index=ix)
    return 'OK', 201
