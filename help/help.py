from lxml import etree
from glob import glob
from pprint import pprint
from io import StringIO
from json import dump
import requests
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


parser = etree.HTMLParser()


def get_links(response, startswith='https://slack.com/help/articles'):
    return set([a.attrib['href'] for a in response.xpath('//a') if 'href' in a.attrib and a.attrib['href'].startswith(startswith)])


def get_urls():
    articles = set()
    for fn in glob('*.html'):
        tree = etree.parse(open(fn), parser)
        articles |= get_links(tree)
    return articles


helps = {}
urls = get_urls()
tot = len(urls)
for i, url in enumerate(urls):
    response = requests.get(url)
    tree = etree.parse(StringIO(response.content.decode('utf-8')), parser)
    title = tree.xpath('//h1[@class="article_title"]')[0].text
    print('%.2f' % (i / tot * 100), title)
    body = tree.xpath('//div[@class="article_body"]')[0]
    content = ''
    for p in body.xpath('//p'):
        content += strip_tags(etree.tostring(p).decode('utf8'))
        content += '\n'
    helps[url] = {'content': content, 'title': title, 'url': url}

with open('helps.json', 'w') as f:
    dump(helps, f)
