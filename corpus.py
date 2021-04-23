from os import getenv, path
from glob import glob
from json import load
from datetime import datetime
from multiprocessing import Pool
from itertools import chain


users = {}

EXPORT_DIR = getenv('EXPORT_DIR', 'messages')


def sec2datetime(seconds, utc=True):
    func = datetime.utcfromtimestamp if utc else datetime.fromtimestamp
    return func(seconds)


def fmt_user(user):
    profile = user['profile']
    return {
        'id': user['id'],
        'is_admin': user.get('is_admin', False),
        'is_owner': user.get('is_owner', False),
        'is_bot': user['is_bot'],
        'is_app_user': user['is_app_user'],
        'display_name': profile['display_name_normalized'],
        'first_name': profile.get('first_name'),
        'last_name': profile.get('last_name'),
        'real_name': profile['real_name_normalized'],
        'image': profile['image_72'],
        'email': profile.get('email'),
        'phone': profile.get('phone'),
    }


def rmcode(txt):
    if '```' not in txt:
        return txt
    i = txt.find('```')
    n = txt.find('```', i + 3)
    txt = txt.replace(txt[i:n + 3], '')
    if '```' in txt:
        return rmcode(txt)
    return txt.strip()


def get_file_messages(fn):
    channel = path.basename(path.dirname(fn))
    msgs = []
    for conv in load(open(fn)):
        if conv['type'] == 'message' and 'text' in conv and conv['text'] and 'client_msg_id' in conv:
            id, user_id, text = conv['client_msg_id'], conv['user'], conv['text']
            ts = sec2datetime(float(conv['ts']))
            if user_id in users:
                user = users[user_id]
            else:
                user = conv.get('user_profile', {})
                user['id'] = user_id
                users[user_id] = user
            msg = {'channel': channel, 'id': id, 'user': user, 'text': text, 'ts': ts}
            # yield msg
            msgs.append(msg)
    return msgs


def get_messages(verbosity=1):
    pool = Pool(10)  # this takes some tuning
    async_result = pool.map_async(get_file_messages, sorted(glob(f'{EXPORT_DIR}/*/*.json')))
    data = async_result.get()
    pool.close()
    return list(chain(*data))


def get_users(limit=None):
    count = 0
    for user in load(open(f'{EXPORT_DIR}/users.json')):
        yield fmt_user(user)
        if limit and count >= limit:
            break


def username_lookup():
    return {user['id']: user['real_name'] for user in get_users()}


def main():
    print(len(get_messages()))
