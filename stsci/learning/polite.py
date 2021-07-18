import csv
import json

from convokit import Classifier, Corpus, TextParser, PolitenessStrategies, download

from stsci.learning.corpus import corp, get_users


wiki_corpus = Corpus(download("wikipedia-politeness-corpus"))
parser = TextParser(verbosity=1000)
wiki_corpus = parser.transform(wiki_corpus)
ps = PolitenessStrategies()
wiki_corpus = ps.transform(wiki_corpus, markers=True)
clf = Classifier(obj_type="utterance",
                 pred_feats=["politeness_strategies"],
                 labeller=lambda utt: utt.meta['Binary'] == 1)
clf.fit(wiki_corpus)


def analyze():
    from convokit import Corpus, Speaker, Utterance, PolitenessStrategies, TextParser
    # user = Speaker(id=user, meta=conv.get('user_profile', {}))
    # utterances.append(Utterance(id=id, speaker=user, text=text, meta={}))
    # corp = Corpus(utterances=utterances)
    # corp = TextParser(verbosity=1000).transform(corp)
    # corp = PolitenessStrategies().transform(corp, markers=True)


# speakers = {1: Speaker(id=1, meta={'name': 'justin'})}
# speakers
# speakers = {'me': Speaker(id='me', meta={'name': 'justin'})}
# utterances = {'hello': Utterance(id='hello', speaker=speakers['me'], text='hello i am pleased to meet you', meta={'nice': True})}
#
# corp = Corpus(utterances=utterances.values())
# clf.transform(corp)
# corp = ps.transform(corp, markers=True)
# parser.transform(corp)
# corp = parser.transform(corp)
# corp = ps.transform(corp, markers=True)
# corp.get_utterance('hello').meta
test_pred = clf.transform(corp)
users = get_users()
with open('polite.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'score', 'text'])
    for u in test_pred.get_utterance_ids():
        u = test_pred.get_utterance(u)
        writer.writerow([users.get(u.speaker.id, u.speaker.id), u.meta["pred_score"], u.text])
        # .speaker.id,test_pred.get_utterance(u).meta['pred_score'],test_pred.get_utterance])
