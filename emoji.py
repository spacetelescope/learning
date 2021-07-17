from corpus import get_messages
from pprint import pprint


EMOJI = ':eyes:'


def main():
    channels = []
    for message in get_messages():
        if message['reactions'] and message['channel'] not in channels:
            channels.append(message['channel'])
    pprint(channels)
    # if EMOJI in message['text']:
    #     print(message['channel'], message['text'])
