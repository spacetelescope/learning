# pip install spacy nltk
# python -m spacy download en_core_web_sm
import ipdb
from collections import Counter
from spacy import displacy
import spacy
from spacy.cli.download import download as spacy_download
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import twitter_samples, stopwords
from pprint import pprint
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import string

ex = 'European authorities fined Google a record $5.1 billion on Wednesday for abusing its power '
'in the mobile phone market and ordered the company to alter its practices. and Fred was to blame for it all. Fred is awful'
pattern = 'NP: {<DT>?<JJ>*<NN>}'


def init():
    nltk.download('punkt')
    nltk.download('twitter_samples')
    nltk.download('wordnet')
    spacy_download('en_core_web_sm')


def remove_noise(tweet_tokens, stop_words=()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def main():

    positive_tweets = twitter_samples.tokenized('positive_tweets.json')
    negative_tweets = twitter_samples.tokenized('negative_tweets.json')

    def get_tweets_for_model(cleaned_tokens_list):
        for tweet_tokens in cleaned_tokens_list:
            yield dict([token, True] for token in tweet_tokens)

    positive_tokens_for_model = get_tweets_for_model(positive_tweets)
    negative_tokens_for_model = get_tweets_for_model(negative_tweets)
    positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                        for tweet_dict in negative_tokens_for_model]
    dataset = positive_dataset + negative_dataset

    nlp = spacy.load("en_core_web_sm")
    classifier = NaiveBayesClassifier.train(dataset)

    sentiments = {T: (T.ent_iob_, T.ent_type_) for T in nlp(ex) if T.ent_type_}
    verdict = classifier.classify({token: True for token in remove_noise(word_tokenize(ex))})
    return verdict, sentiments


def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

    # doc = nlp(ex)
    # filtered_tokens = [token for token in doc if not token.is_stop]


def xtra():
    sent = preprocess(ex)
    cp = nltk.RegexpParser(pattern)
    cs = cp.parse(sent)
    print(cs)

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(ex)
    pprint([(X.text, X.label_) for X in doc.ents])
    pprint([(X, X.ent_iob_, X.ent_type_) for X in doc])
    items = [x.text for x in doc.ents]
    print(dict([(str(x), x.label_) for x in doc.ents]))

    return Counter(items).most_common(3)
