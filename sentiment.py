import csv
# from multiprocessing import Pool

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


def analyze_words(words):
    tags, newwords = [], []
    for word in words:
        lword = word.lower()
        if lword in STOPWORDS:
            continue
        if lword.startswith('<http'):
            continue
        try:
            # ignore hex text
            int(lword, 16)
            continue
        except ValueError:
            pass
        if word.startswith('<@W'):
            user = lword[2:11].upper()
            if user in usernames:
                user = usernames[user]
            tags.append(f'{user}(PERSON)')
            newwords.append(user)
            continue
        if not word[0].isalnum():
            continue
        if lword in tag_lookup:
            tags.append(tag_lookup[lword])
            continue
        newwords.append(word)
    doc = nlp(' '.join(newwords))
    for ent in doc.ents:
        if ent.label_.lower() in IGNORE:
            continue
        if not ent.text.isalnum():
            continue
        if ent.text.isnumeric():
            continue
        tags.append(f'{ent.text}({ent.label_})')
    return tags, newwords


def analyze(txt):
    sent_text = nltk.sent_tokenize(txt)
    tags = []
    for sentence in sent_text:
        scores = sia.polarity_scores(sentence)
        tags, words = analyze_words(sentence.split())
        if 'service desk' in sentence:
            tags.append('ServiceDesk(ORG)')
        yield scores['compound'], set(tags), words


def fmt_msg(msg):
    txt = msg['text']
    if '```' in txt:
        txt = rmcode(txt)
    if not txt:
        return []
    rows = []
    for score, tags, words in analyze(txt):
        if not tags or not score:
            return []
        user = msg['user']['id']
        if user in usernames:
            user = usernames[user]
        rows.append([msg['ts'], msg['channel'], user, score, '|'.join(tags), ' '.join(words)])
    return rows


def main():
    # with Pool() as pool:
    #     async_result = pool.map_async(fmt_msg, get_messages()[:100])
    #     data = filter(None, async_result.get())
    data = []
    for msg in get_messages(100):
        data.extend(fmt_msg(msg))

    with open('msg.sentiment.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Time', 'Channel', 'User', 'Score', 'Tags', 'Text'])
        writer.writerows(data)


if __name__ == '__main__':
    main()
