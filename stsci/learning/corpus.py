from os import path
from glob import glob
from json import load
from datetime import datetime
from multiprocessing import Pool
from itertools import chain

from stsci.learning.log import logger
from stsci.learning.settings import POOL, EXPORT_DIR


users = {}


def globber(*paths):
    return sorted(glob(path.join(EXPORT_DIR, *paths)))


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
    """Remove code blocks from markdown text"""
    if '```' not in txt:
        return txt
    i = txt.find('```')
    n = txt.find('```', i + 3)
    if n == -1:
        return txt.replace('```', '')
    txt = txt.replace(txt[i:n + 3], '')
    if '```' in txt:
        return rmcode(txt)
    return txt.strip()


def get_file_messages(fn, verbosity=0):
    """Returns a list of messages from an individual JSON file"""
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
            msg = {'channel': channel, 'id': id, 'user': user, 'text': text, 'ts': ts, 'reactions': conv.get('reactions', [])}
            # yield msg
            if verbosity > 1:
                logger.debug(msg)
            msgs.append(msg)
    return msgs


def get_messages(limit=None, pool=POOL, verbosity=0):
    """
    Returns a list of messages from the export

    limit: int to limit the length of response
    pool: bool to use multiprocess pooling
    verbosity: raise logging level
    """
    if pool:
        with Pool() as procpool:
            async_result = procpool.map_async(get_file_messages, globber('*', '*.json'), verbosity)
            data = async_result.get()
        return list(chain(*data))[:limit]
    msgs = []
    for file_name in globber('*', '*.json'):
        if verbosity > 0:
            logger.info(f'Loading file {file_name}')
        file_msgs = get_file_messages(file_name, verbosity)
        if verbosity > 1:
            logger.info(f'Loaded {len(file_msgs)} messages file')
        msgs.extend(file_msgs)
        if limit and len(msgs) >= limit:
            return msgs[:limit]
    return msgs


def get_users(limit=None):
    """
    Returns a list of users from the export

    limit: int to limit the length of response
    """
    count = 1
    for user in load(open(f'{EXPORT_DIR}/users.json')):
        yield fmt_user(user)
        if limit and count >= limit:
            break
        count += 1


def fmt_channel(channel, users):
    chan = {'id': channel['id'], 'name': channel['name'], 'created_at': channel['created']}
    if users:
        chan['users'] = channel['members']
    return chan


def get_channels(limit=None, users=False):
    """
    Returns a list of channels from the export

    limit: int to limit the length of response
    """
    count = 1
    for channel in load(open(f'{EXPORT_DIR}/channels.json')):
        yield fmt_channel(channel, users)
        if limit and count >= limit:
            break
        count += 1


def username_lookup():
    return {user['id']: user['real_name'] for user in get_users()}
