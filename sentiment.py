import json
from glob import glob
from pprint import pprint
from statistics import mean

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from spacy import displacy
from collections import Counter
import en_core_web_sm
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

nlp = en_core_web_sm.load()
# pipenv run python -m nltk.downloader averaged_perceptron_tagger punkt
# pipenv run python -m spacy download en_core_web_sm
pattern = 'NP: {<DT>?<JJ>*<NN>}'
cp = nltk.RegexpParser(pattern)
stopwords = nltk.corpus.stopwords.words("english")


def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return cp.parse(sent)


text = 'European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices.'

# print(preprocess(text))
# words = nltk.word_tokenize(text)
# text = nltk.Text(words)
# fd = text.vocab()
# print(fd.tabulate(3))

# print(sia.polarity_scores(text))


#
ignore = ['date', 'time', 'percent', 'money', 'quantity', 'ordinal', 'cardinal', 'work_of_art']
entities = {}
for fn in glob('export/*/*.json'):
    for data in json.load(open(fn)):
        if 'text' not in data:
            continue
        text = data['text']
        words = [w for w in text.split() if w.lower() not in stopwords]
        scores = sia.polarity_scores(text)
        # if .3 > scores['compound'] > -.3:
        #     continue
        doc = nlp(' '.join(words))
        for ent in doc.ents:
            if ent.label_.lower() in ignore:
                continue
            k = '%s(%s)' % (ent.text, ent.label_)
            entities.setdefault(k, [])
            entities[k].append(scores['compound'])
with open('sentiment.json', 'w') as f:
    json.dump({k: mean(v) for k, v in entities.items()}, f)
