from glob import glob
from json import load


users = {}


def get_messages(limit=None):
    for i, fn in enumerate(glob('messages/*/*.json')):
        for conv in load(open(fn)):
            if conv['type'] == 'message' and 'text' in conv and conv['text'] and 'client_msg_id' in conv:
                id, user, text = conv['client_msg_id'], conv['user'], conv['text']
                if user in users:
                    user = users[user]
                else:
                    user = conv.get('user_profile', {})
                    users[conv['user']] = user
                yield {'id': id, 'user': user, 'text': text}
        if limit and i >= limit:
            break


def get_users():
    return load(open('users.json'))
