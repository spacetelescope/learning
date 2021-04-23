import csv

import nltk
from spacy import load
from nltk.sentiment import SentimentIntensityAnalyzer

from corpus import get_messages

sia = SentimentIntensityAnalyzer()

nlp = load("en_core_web_lg")
# pipenv run python -m nltk.downloader averaged_perceptron_tagger punkt
# pipenv run python -m spacy download en_core_web_sm
STOPWORDS = nltk.corpus.stopwords.words("english")

IGNORE = ['date', 'time', 'percent', 'money', 'quantity', 'ordinal', 'cardinal', 'work_of_art']


def analyze(txt):
    tags = []
    scores = sia.polarity_scores(txt)
    words = []
    for word in txt.split():
        lword = word.lower()
        if lword in STOPWORDS:
            continue
        if lword.startswith('<http'):
            continue
        if word.startswith('<@W'):
            word = lword[2:11].upper()
            tags.append(f'{word}(PERSON)')
        if not word[0].isalnum():
            continue
        if lword == 'stars':
            tags.append('STARS(ORG)')
        if lword == 'itsd':
            tags.append('ITSD(ORG)')
        if lword == 'servicedesk':
            tags.append('ServiceDesk(ORG)')
        if lword == 'stsci':
            tags.append('STScI(ORG)')
        if lword == 'myst':
            tags.append('MyST(PRODUCT)')
        words.append(word)
    if 'service desk' in txt:
        tags.append('ServiceDesk(ORG)')
    doc = nlp(' '.join(words))
    for ent in doc.ents:
        if ent.label_.lower() in IGNORE:
            continue
        if not ent.text.isalnum():
            continue
        tags.append(f'{ent.text}({ent.label_})')
    return scores['compound'], set(tags)


def main():
    with open('msg.sentiment.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Time', 'Channel', 'Score', 'Tags', 'Text'])
        for msg in get_messages():
            score, tags = analyze(msg['text'])
            if not tags or not score:
                continue
            txt = msg['text'].replace('"', "'").replace('\n', '').replace('\r', '')[:1000]
            writer.writerow([msg['ts'], msg['channel'], score, '|'.join(tags), txt])


if __name__ == '__main__':
    main()
