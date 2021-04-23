import csv
from multiprocessing import Pool

import nltk
from spacy import load
from nltk.sentiment import SentimentIntensityAnalyzer

from corpus import get_messages, username_lookup, rmcode

sia = SentimentIntensityAnalyzer()

nlp = load("en_core_web_lg")
# pipenv run python -m nltk.downloader averaged_perceptron_tagger punkt
# pipenv run python -m spacy download en_core_web_sm
STOPWORDS = nltk.corpus.stopwords.words("english")

IGNORE = ['date', 'time', 'percent', 'money', 'quantity', 'ordinal', 'cardinal', 'work_of_art']

usernames = username_lookup()

tag_lookup = {
    'stars': 'STARS(ORG)',
    'itsd': 'ITSD(ORG)',
    'servicedesk': 'ServiceDesk(ORG)',
    'stsci': 'STScI(ORG)',
    'myst': 'MyST(PRODUCT)',
    'sso': 'SSO(PRODUCT)',
}


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
            user = lword[2:11].upper()
            if user in usernames:
                user = usernames[user]
            tags.append(f'{user}(PERSON)')
            words.append(user)
            continue
        if not word[0].isalnum():
            continue
        if lword in tag_lookup:
            tags.append(tag_lookup[lword])
            continue
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


def fmt_msg(msg):
    txt = msg['text']
    if '```' in txt:
        txt = rmcode(txt)
    if not txt:
        return
    score, tags = analyze(txt)
    if not tags or not score:
        return
    user = msg['user']['id']
    if user in usernames:
        user = usernames[user]
    txt = txt.replace('"', "'").replace('\n', '').replace('\r', '')[:1000]
    return [msg['ts'], msg['channel'], user, score, '|'.join(tags), txt]


def main():

    pool = Pool()  # this takes some tuning
    async_result = pool.map_async(fmt_msg, get_messages())
    data = filter(None, async_result.get())
    pool.close()
    with open('msg.sentiment.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Time', 'Channel', 'User', 'Score', 'Tags', 'Text'])
        writer.writerows(data)


if __name__ == '__main__':
    main()
