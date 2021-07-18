from json import dump
from pprint import pprint

from ipdb import launch_ipdb_on_exception

from stsci.learning.entity import classify
from stsci.learning.corpus import get_messages


speakers = {'Positive': {}, 'Negative': {}}
entities = {'Positive': {}, 'Negative': {}}
for message in get_messages():
    speaker, txt = message['speaker'], message['text']
    if not speaker:
        continue
    verdict, attrs = classify(txt)
    speakers[verdict].setdefault(speaker['display_name'], 0)
    speakers[verdict][speaker['display_name']] += 1
    # for name, tags in attrs.items():
    #     entities[verdict][name.text] = tags

# pprint(speakers)
# pprint(entities)
with launch_ipdb_on_exception():
    with open('sentspeakers.json', 'w') as f:
        dump(speakers, f)
